import asyncio
from src.constants import uscis_database, uscis_table_name
from src.db_stuff import connect_to_database, drop_table, build_table, insert_entry, \
    get_all, get_all_case, update_case
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
                old_message = rep[0]['history']
                print(old_message)
                new_message = "|".join([message, old_message]) if old_message else message
                rep2 = await update_case(conn=conn, table_name=test_table_name, case_number=receipt_number,
                                         last_updated=timestamp,
                                         current_status=title,
                                         history=new_message
                                         )
                print(rep2)
            else:
                print()
                await insert_entry(conn=conn, table_name=test_table_name,
                                   case_number=receipt_number,
                                   last_updated=timestamp,
                                   current_status=title,
                                   history=message)

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

        for i in range(2015550256, 2015550260):
            await test_number(number=i)
        await test_number(number=2015550256)

    finally:
        await conn.close()

asyncio.get_event_loop().run_until_complete(main())
