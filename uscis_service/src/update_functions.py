import aiohttp
import asyncio
import datetime
import itertools
from src.constants import uscis_database, uscis_table_name, error_table_name
from src.db_stuff import connect_to_database, build_table, insert_entry, \
    get_all, get_all_case, update_case, delete_case, get_all_status, read_db, drop_table
from src.message_stuff import string_to_args, get_arguments_from_string, rebuild_string_from_template, \
    args_to_string, remove_tags, check_title_in_status, get_template, status_to_msg
from src.parse_site import check as uscis_check


async def update_case_internal(conn, url_session, receipt_number, skip_recent_threshold=10):
    # print(f"update_case_internal - Updating {receipt_number}\t")
    rep = await get_all_case(conn=conn, table_name=uscis_table_name, case_number=receipt_number)
    if rep and skip_recent_threshold:
        current_status = rep[0]['current_status']
        current_timestamp = rep[0]['last_updated']
        if current_status is not None:  # and current_status != "CASE STATUS":
            age = datetime.datetime.utcnow() - current_timestamp
            # print(f"Age of status:\t{age}\t\t{current_timestamp}\t\t{datetime.datetime.utcnow()}")
            if age < datetime.timedelta(hours=skip_recent_threshold):
                msg = f"\tAge of status:\t{age} - Request not sent - {receipt_number}"
                return msg
            if current_status in [
                "Card Was Delivered To Me By The Post Office",
                "Case Was Approved",
                "Case Was Approved And My Decision Was Emailed",
            ]:
                msg = f"\t{current_status} - Request not sent - {receipt_number}"
                return msg
    # print(f"\t\tupdate_case_internal - Requesting {receipt_number}\t")
    timestamp, title, message = await uscis_check(url_session=url_session, receipt_number=receipt_number)
    # print(f"\t\t\tupdate_case_internal - Result {receipt_number}\t{title} - {message}")

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
                    f"Message recomposition string is wrong\n\t\tClean\t{clean_string}\n\t\tRebuilt\t{rebuild_string}"
                    f"\n\t\t{message}"
                    f"\n\t\t{title}\t\t{current_args}"
                )
        if not rep:
            await insert_entry(conn=conn, table_name=uscis_table_name,
                               case_number=receipt_number,
                               last_updated=timestamp,
                               current_status=title,
                               current_args=current_args,
                               history="")
        else:
            old_status = rep[0]['current_status']
            old_args = rep[0]['current_args']
            old_history = rep[0]['history']
            if title == "CASE STATUS" and old_status is not None and old_status != "CASE STATUS":
                # raise AttributeError(
                print(
                    f"New Status is CASE STATUS although old status was different:\t{old_status}"
                    f"\t\t{receipt_number}"
                    f"\t\told_args:\t{old_args}"
                    f"\t\tnew message:\t{message}"
                )
            if (old_status, old_args) == (title, current_args) or old_status is None:
                new_history_joined = old_history
            else:
                new_history = ":".join([old_status, old_args])
                new_history_joined = "||".join([new_history, old_history]) if old_history else new_history
            await update_case(conn=conn, table_name=uscis_table_name,
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


async def update_entries(it, skip_recent_threshold=10, chunk_size=100):
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            await build_table(conn=conn, table_name=uscis_table_name)
            await build_table(conn=conn, table_name=error_table_name)

        async with aiohttp.ClientSession() as session:
            async def update_function(case):
                async with pool.acquire() as conn2:
                    await update_case_internal(conn=conn2, url_session=session, receipt_number=case,
                                               skip_recent_threshold=skip_recent_threshold)

            it_t = iter(it)
            i = 0
            while True:
                chunk = tuple(itertools.islice(it_t, chunk_size))
                print(f"update_entries chunk number {i}\t\t-\t{datetime.datetime.now()}")
                i += 1
                if not chunk:
                    break
                await asyncio.gather(*map(update_function, chunk))

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
            await read_db(conn=conn, table_name=uscis_table_name, len_only=True)
    finally:
        await pool.close()


async def refresh_status(status, skip_recent_threshold=0, chunk_size=100):
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            old_status = await get_all_status(conn=conn, table_name=uscis_table_name, status=status)
            old_cases = [row['case_number'] for row in old_status]
            print("Refreshing", status, len(old_status))
    finally:
        await pool.close()
    await update_entries(old_cases, skip_recent_threshold=skip_recent_threshold, chunk_size=chunk_size)
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn2:
            new_status = await get_all_status(conn=conn2, table_name=uscis_table_name, status=status)
            conclusion = "Unchanged" if len(old_status) == len(new_status) \
                else f"Reduced by {len(old_status) - len(new_status)}"
            print("Refreshing Results", status, f"{len(old_status)} to {len(new_status)}\t---\t{conclusion}")
    finally:
        await pool.close()


async def refresh_selected_status(filter_function=lambda x: x < 100, skip_recent_threshold=0):
    pool = await connect_to_database(database=uscis_database)
    async with pool.acquire() as connection:
        rep = await get_all(conn=connection, table_name=uscis_table_name, ignore_null=True)
        print(f"Number of entries {len(rep)}")

        status_number = {}
        for status in status_to_msg:
            rep_status = await get_all_status(conn=connection, status=status, table_name=uscis_table_name)
            status_number[status] = len(rep_status)

        for status, length in sorted(status_number.items(), key=lambda k: k[1], reverse=True):
            if length and filter_function(length):
                await refresh_status(status=status, skip_recent_threshold=skip_recent_threshold)
                print()


async def refresh_error():
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            old_status = await get_all(conn=conn, table_name=error_table_name)
            old_cases = [row['case_number'] for row in old_status]
            print("Refreshing errors")
        await update_entries(old_cases, skip_recent_threshold=0, chunk_size=100)
        async with pool.acquire() as conn:
            new_status = await get_all(conn=conn, table_name=error_table_name)
            print("Refreshing Errors - result", f"{len(old_status)} to {len(new_status)}")
    finally:
        await pool.close()


async def smart_update_all_function(
        pool, prefix="LIN", year_start=20, day_start=1, skip_recent_threshold=10, chunk_size=100
):

    async with aiohttp.ClientSession() as session:

        def current_format(index):
            return format_receipt_number(
                year=year_start + year_increment,
                day=day_start + day_increment,
                index=index,
            )

        async def update_function(index):
            async with pool.acquire() as conn2:
                return await update_case_internal(
                    conn=conn2, url_session=session,
                    receipt_number=current_format(index=index),
                    skip_recent_threshold=skip_recent_threshold,
                )

        async def inside_loop():
            index_increment = 0
            all_none = False
            while not all_none:
                print(f"smart update -\t"
                      f"{current_format(index=index_start+index_increment)}\t"
                      f"\t{datetime.datetime.now()}")
                rep = await asyncio.gather(
                    *map(update_function, [index_start + index_increment + i for i in range(chunk_size)])
                )
                all_none = all(s is None for s in rep)
                index_increment += chunk_size

        if day_start == 0:
            def format_receipt_number(year, day, index):
                return f'{prefix}{year:02d}9{index:07d}'

            index_start = 1
            year_increment = 0
            while await update_function(index=index_start) is not None:
                await inside_loop()
                year_increment += 1
        else:
            def format_receipt_number(year, day, index):
                return f'{prefix}{year:02d}{day:03d}5{index:04d}'

            index_start = 1
            year_increment = 0
            while await update_function(index=index_start) is not None:
                day_increment = 0
                while await update_function(index=index_start) is not None:
                    await inside_loop()
                    day_increment += 1
                year_increment += 1


async def smart_update_all(
        prefix="LIN", year_start=20, day_start=1, skip_recent_threshold=10, chunk_size=100,
):
    """
    prefix: 3 letter-string, represents the center location
    year_start: 2 digit in representing the year - "20" for FY2019-2020 - FY starts on 1st Oct
    day_start: 1 to 326 (should be the number of business days - I don't know why it's so high) -> index of day in FY
                0 -> another representation : LIN2090000001
    skip_recent_threshold: don't refresh if last refresh was more recent than x hours
    chunk_size: size of chunk in the loop
    """
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            await build_table(conn=conn, table_name=uscis_table_name)
            await build_table(conn=conn, table_name=error_table_name)

        await smart_update_all_function(
            pool=pool, prefix=prefix, year_start=year_start, day_start=day_start,
            skip_recent_threshold=skip_recent_threshold,
            chunk_size=chunk_size,
        )

        async with pool.acquire() as conn:
            await read_db(conn=conn, table_name=uscis_table_name, len_only=True)
            await read_db(conn=conn, table_name=error_table_name)
    finally:
        await pool.close()


async def clear_uscis_table():
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            await drop_table(conn=conn, table_name=uscis_table_name)
            await build_table(conn=conn, table_name=uscis_table_name)
            await build_table(conn=conn, table_name=error_table_name)
    finally:
        await pool.close()
