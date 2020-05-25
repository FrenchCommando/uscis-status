import asyncio
from src.constants import uscis_database, uscis_table_name
from src.db_stuff import connect_to_database, drop_table, build_table, insert_entry, \
    get_all, get_all_case, update_case
from src.message_stuff import string_to_args, get_arguments_from_string, rebuild_string_from_template, args_to_string
from src.parse_site import check as uscis_check


async def main():
    conn = await connect_to_database(database=uscis_database)
    test_table_name = f"test_{uscis_table_name}"
    try:
        await drop_table(conn=conn, table_name=test_table_name)
        await build_table(conn=conn, table_name=test_table_name)

        async def update_case_internal(receipt_number):
            rep = await get_all_case(conn=conn, table_name=test_table_name, case_number=receipt_number)
            timestamp, title, message = uscis_check(receipt_number=receipt_number)
            if rep:
                print(rep)
                current_args = args_to_string(d=get_arguments_from_string(s=message, status=title))
                old_status = rep[0]['current_status']
                old_args = rep[0]['current_args']
                old_history = rep[0]['history']
                if (old_status, old_args) == (title, current_args):
                    new_history_joined = old_history
                else:
                    new_history = ":".join([title, current_args])
                    new_history_joined = "||".join([new_history, old_history]) if old_history else new_history
                rep2 = await update_case(conn=conn, table_name=test_table_name, case_number=receipt_number,
                                         last_updated=timestamp,
                                         current_status=title,
                                         current_args=current_args,
                                         history=new_history_joined
                                         )
                print(rep2)
            else:
                print()
                current_args = args_to_string(d=get_arguments_from_string(s=message, status=title))
                print(message == rebuild_string_from_template(status=title, **string_to_args(s=current_args)))

                await insert_entry(conn=conn, table_name=test_table_name,
                                   case_number=receipt_number,
                                   last_updated=timestamp,
                                   current_status=title,
                                   current_args=current_args,
                                   history="")

        async def read_db():
            row = await get_all(conn=conn, table_name=test_table_name)
            for u in row:
                print(u)
            print(len(row))

        prefix = "LIN"

        async def test_number(number):
            print(number)
            await update_case_internal(receipt_number=f"{prefix}{number}")
            await read_db()
            print()

        for i in [
            2015550361,  # Case Was Received
            2015550363,  # Case Was Received
            2015550362,  # Case Was Approved
            2015550364,  # Case Was Approved
            2015550360,  # Request for Additional Evidence Was Sent
            2015550064,  # Request for Additional Evidence Was Sent
            2015550361,  # Case Was Received - re
        ]:
            await test_number(number=i)
        for i in range(2015550164, 2015550169):
            await test_number(number=i)

    finally:
        await conn.close()

asyncio.get_event_loop().run_until_complete(main())
