from src.constants import uscis_database, uscis_table_name, error_table_name
from src.db_stuff import connect_to_database, drop_table, build_table, insert_entry, \
    get_all, get_all_case, update_case, delete_case, get_all_status
from src.message_stuff import string_to_args, get_arguments_from_string, rebuild_string_from_template, \
    args_to_string, remove_tags, check_title_in_status, get_template
from src.parse_site import check as uscis_check


async def read_db(conn, table_name):
    row = await get_all(conn=conn, table_name=table_name)
    print(len(row))
    for u in row:
        print(u)


async def update_case_internal(conn, receipt_number):
    print("Updating", receipt_number, "\t")
    ignored_cases = ['LIN2000150095']  # formatting is wrong - can't match the template
    if receipt_number in ignored_cases:
        print("Ignored - skip", receipt_number)
        return "Ignored"
    rep = await get_all_case(conn=conn, table_name=uscis_table_name, case_number=receipt_number)
    if rep and rep[0]['current_status'] == "Case Was Approved":
        msg = "Case Was Approved - Request not sent"
        print(msg)
        return msg
    timestamp, title, message = uscis_check(receipt_number=receipt_number)
    print(title)
    if rep:
        try:
            current_args = args_to_string(d=get_arguments_from_string(s=message, status=title))
            old_status = rep[0]['current_status']
            old_args = rep[0]['current_args']
            old_history = rep[0]['history']
            if (old_status, old_args) == (title, current_args):
                new_history_joined = old_history
            else:
                new_history = ":".join([old_status, old_args])
                new_history_joined = "||".join([new_history, old_history]) if old_history else new_history
            await update_case(conn=conn, table_name=uscis_table_name, case_number=receipt_number,
                              last_updated=timestamp,
                              current_status=title,
                              current_args=current_args,
                              history=new_history_joined
                              )
            await delete_case(conn=conn, table_name=error_table_name, case_number=receipt_number)
        except AttributeError as e:
            await insert_entry(conn, error_table_name, title=title, case_number=receipt_number, message=message)
            await read_db(conn=conn, table_name=error_table_name)
            print("Message format error", title, e)
            print(remove_tags(s=message))
            print(get_template(title))
    else:
        if not check_title_in_status(title=title):
            await insert_entry(conn, error_table_name, title=title, case_number=receipt_number, message=message)
            await read_db(conn=conn, table_name=error_table_name)
        else:
            try:
                current_args = args_to_string(d=get_arguments_from_string(s=message, status=title))
                if title is not None:
                    if not (remove_tags(s=message)
                            == rebuild_string_from_template(status=title, **string_to_args(s=current_args))):
                        print("Error Here")
                        print("\t", message)
                        print("\t", title, current_args)
                await insert_entry(conn=conn, table_name=uscis_table_name,
                                   case_number=receipt_number,
                                   last_updated=timestamp,
                                   current_status=title,
                                   current_args=current_args,
                                   history="")
                await delete_case(conn=conn, table_name=error_table_name, case_number=receipt_number)
            except AttributeError as e:
                await insert_entry(conn=conn, table_name=error_table_name,
                                   title=title, case_number=receipt_number, message=message)
                await read_db(conn=conn, table_name=error_table_name)
                print("Message format error", title, e)
                print(remove_tags(s=message))
                print(get_template(title))

    return title


async def remove_case_internal(conn, receipt_number):
    print("Removing", receipt_number)
    rep = await get_all_case(conn=conn, table_name=uscis_table_name, case_number=receipt_number)
    if rep:
        await delete_case(conn=conn, table_name=uscis_table_name, case_number=receipt_number)
    else:
        print("Removing failed, Entry does not exist")
    await drop_table(conn=conn, table_name=error_table_name)
    await build_table(conn=conn, table_name=error_table_name)
    await delete_case(conn=conn, table_name=error_table_name, case_number=receipt_number)


async def update_entries(it):
    conn = await connect_to_database(database=uscis_database)
    try:
        await build_table(conn=conn, table_name=uscis_table_name)
        await build_table(conn=conn, table_name=error_table_name)
        for case in it:
            await update_case_internal(conn=conn, receipt_number=case)
        await read_db(conn=conn, table_name=uscis_table_name)
        await read_db(conn=conn, table_name=error_table_name)
    finally:
        await conn.close()


async def delete_entries(it):
    conn = await connect_to_database(database=uscis_database)
    try:
        for case in it:
            await remove_case_internal(conn=conn, receipt_number=case)
        await read_db(conn=conn, table_name=uscis_table_name)
    finally:
        await conn.close()


async def refresh_case(status, delete=False):  # delete all cases for a given status, and reloads them
    conn = await connect_to_database(database=uscis_database)
    try:
        old_status = await get_all_status(conn=conn, table_name=uscis_table_name, status=status)
        old_cases = [row['case_number'] for row in old_status]
        print("Refreshing", status)
        for case in old_cases:
            print("Refreshing case", case)
            if delete:
                await remove_case_internal(conn=conn, receipt_number=case)
            await update_case_internal(conn=conn, receipt_number=case)
        await read_db(conn=conn, table_name=uscis_table_name)
    finally:
        await conn.close()


async def refresh_error(status, delete=False):
    conn = await connect_to_database(database=uscis_database)
    try:
        old_status = await get_all(conn=conn, table_name=error_table_name)
        old_cases = [row['case_number'] for row in old_status]
        print("Refreshing", status)
        for case in old_cases:
            print("Refreshing case", case)
            if delete:
                await remove_case_internal(conn=conn, receipt_number=case)
            await update_case_internal(conn=conn, receipt_number=case)
        await read_db(conn=conn, table_name=uscis_table_name)
    finally:
        await conn.close()


async def smart_update_all(prefix="LIN", date_start=20001, index_start=50001):
    conn = await connect_to_database(database=uscis_database)
    try:
        await build_table(conn=conn, table_name=uscis_table_name)
        await build_table(conn=conn, table_name=error_table_name)

        date_increment = 0
        while (await update_case_internal(
                conn=conn,
                receipt_number=f'{prefix}{date_start + date_increment}{index_start}'
        ) is not None):
            index_increment = 1
            while(await update_case_internal(
                    conn=conn,
                    receipt_number=f'{prefix}{date_start+date_increment}{index_start+index_increment}'
            ) is not None):
                index_increment += 1
            date_increment += 1
        await read_db(conn=conn, table_name=uscis_table_name)
        await read_db(conn=conn, table_name=error_table_name)
    finally:
        await conn.close()
