import aiohttp
import asyncio
from src.constants import uscis_database, uscis_table_name, error_table_name, test_uscis_table
from src.db_stuff import connect_to_database, build_table, insert_entry, \
    get_all, get_all_case, update_case, delete_case, get_all_status
from src.message_stuff import string_to_args, get_arguments_from_string, rebuild_string_from_template, \
    args_to_string, remove_tags, check_title_in_status, get_template
from src.parse_site import check as uscis_check


async def read_db(conn, table_name, len_only=False):
    row = await get_all(conn=conn, table_name=table_name)
    if not len_only:
        for u in row:
            print(u)
    print(len(row))


async def update_case_internal(conn, url_session, receipt_number, skip_existing=False, test_table=False):
    uscis_table = uscis_table_name if not test_table else test_uscis_table
    print(f"update_case_internal - Updating {receipt_number}\t")
    rep = await get_all_case(conn=conn, table_name=uscis_table, case_number=receipt_number)
    if rep and rep[0]['current_status'] is not None and skip_existing:
        msg = f"\t{rep[0]['current_status']} - Request not sent"
        print(msg)
        return msg
    print(f"\t\tupdate_case_internal - Requesting {receipt_number}\t")
    timestamp, title, message = await uscis_check(url_session=url_session, receipt_number=receipt_number)
    print(f"\t\t\tupdate_case_internal - Result {receipt_number}\t{title} - {message}")

    async def handle_error(error=None):
        await insert_entry(conn, error_table_name, title=title, case_number=receipt_number, message=message)
        print(f"Something went wrong -\n\treceipt_number:\t{receipt_number}\n\tstatus:\t{title}\n\tmessage:\t{message}")
        print(f"\t\tError message:\t{error}")
        print(f"\t\tClean msg:\t{remove_tags(s=message)}")
        print(f"\t\tTemplate format:\t{get_template(status=title)}")
        return "Something went Wrong"

    try:
        if not check_title_in_status(title=title):
            raise AttributeError("Title not in Status")
        current_args = args_to_string(d=get_arguments_from_string(s=message, status=title))
        if title is not None:
            clean_string = remove_tags(s=message)
            rebuild_string = rebuild_string_from_template(status=title, **string_to_args(s=current_args))
            if not (clean_string == rebuild_string):
                raise AttributeError(
                    f"Message recomposition string is wrong\n\t\t{clean_string}\n\t\t{rebuild_string}"
                    f"\n\t\t{message}"
                    f"\n\t\t{title}\t\t{current_args}"
                )
        if not rep:
            await insert_entry(conn=conn, table_name=uscis_table,
                               case_number=receipt_number,
                               last_updated=timestamp,
                               current_status=title,
                               current_args=current_args,
                               history="")
        else:
            old_status = rep[0]['current_status']
            old_args = rep[0]['current_args']
            old_history = rep[0]['history']
            if (old_status, old_args) == (title, current_args) or old_status is None:
                new_history_joined = old_history
            else:
                new_history = ":".join([old_status, old_args])
                new_history_joined = "||".join([new_history, old_history]) if old_history else new_history
            await update_case(conn=conn, table_name=uscis_table,
                              case_number=receipt_number,
                              last_updated=timestamp,
                              current_status=title,
                              current_args=current_args,
                              history=new_history_joined
                              )
        await delete_case(conn=conn, table_name=error_table_name, case_number=receipt_number)
        return title
    except BaseException as e:
        return await handle_error(error=e)


async def remove_case_internal(conn, receipt_number):
    print("Removing", receipt_number)
    rep = await get_all_case(conn=conn, table_name=uscis_table_name, case_number=receipt_number)
    if rep:
        await delete_case(conn=conn, table_name=uscis_table_name, case_number=receipt_number)
    else:
        print("Removing failed, Entry does not exist")
    await delete_case(conn=conn, table_name=error_table_name, case_number=receipt_number)


async def update_entries(it, test_table=False):
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            await build_table(conn=conn, table_name=uscis_table_name)
            await build_table(conn=conn, table_name=error_table_name)
        async with aiohttp.ClientSession() as session:
            async def update_function(case):
                async with pool.acquire() as conn2:
                    await update_case_internal(
                        conn=conn2, url_session=session, receipt_number=case, test_table=test_table
                    )
            await asyncio.gather(*map(update_function, it))
        async with pool.acquire() as conn:
            await read_db(conn=conn, table_name=uscis_table_name, len_only=True)
            await read_db(conn=conn, table_name=error_table_name)
    finally:
        await pool.close()


async def delete_entries(it):
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            for case in it:
                await remove_case_internal(conn=conn, receipt_number=case)
            await read_db(conn=conn, table_name=uscis_table_name)
    finally:
        await pool.close()


async def refresh_case(status):
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            old_status = await get_all_status(conn=conn, table_name=uscis_table_name, status=status)
            old_cases = [row['case_number'] for row in old_status]
            print("Refreshing", status, len(old_status))
    finally:
        await pool.close()
    await update_entries(old_cases)
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn2:
            new_status = await get_all_status(conn=conn2, table_name=uscis_table_name, status=status)
            print("Refreshing Results", status, f"{len(old_status)} to {len(new_status)}")
    finally:
        await pool.close()


async def refresh_error(test_table=False):
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            old_status = await get_all(conn=conn, table_name=error_table_name)
            old_cases = [row['case_number'] for row in old_status]
            print("Refreshing errors")
        await update_entries(old_cases, test_table=test_table)
        async with pool.acquire() as conn:
            if test_table:
                await read_db(conn=conn, table_name=test_uscis_table)
            new_status = await get_all(conn=conn, table_name=error_table_name)
            print("Refreshing Errors - result", f"{len(old_status)} to {len(new_status)}")
    finally:
        await pool.close()


async def smart_update_all_function(
        pool, prefix="LIN", date_start=20001, index_start=50001, skip_existing=False, chunk_size=10):
    date_increment = 0
    async with aiohttp.ClientSession() as session:
        async def update_function(index):
            async with pool.acquire() as conn2:
                return await update_case_internal(
                    conn=conn2, url_session=session, receipt_number=f'{prefix}{date_start + date_increment}{index}',
                    skip_existing=skip_existing, test_table=False,
                )
        while await update_function(index=index_start) is not None:
            index_increment = 1
            all_none = False
            while not all_none:
                rep = await asyncio.gather(
                    *map(update_function,
                         [index_start + index_increment + i for i in range(chunk_size)])
                )
                all_none = all(s is None for s in rep)
                index_increment += chunk_size
            date_increment += max(1, index_increment // 100000)


async def smart_update_all(prefix="LIN", date_start=20001, index_start=50001, skip_existing=False, chunk_size=10):
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            await build_table(conn=conn, table_name=uscis_table_name)
            await build_table(conn=conn, table_name=error_table_name)

        await smart_update_all_function(
            pool,
            prefix,
            date_start,
            index_start,
            skip_existing,
            chunk_size)

        async with pool.acquire() as conn:
            await read_db(conn=conn, table_name=uscis_table_name, len_only=True)
            await read_db(conn=conn, table_name=error_table_name)
    finally:
        await pool.close()
