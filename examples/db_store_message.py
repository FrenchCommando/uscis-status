import asyncio
from src.constants import uscis_database, uscis_table_name
from src.db_stuff import connect_to_database, drop_table, build_table, insert_entry, get_all
from src.parse_site import check as uscis_check


async def main():
    conn = await connect_to_database(database=uscis_database)
    test_table_name = f"test_{uscis_table_name}"
    try:
        await drop_table(conn=conn, table_name=test_table_name)
        await build_table(conn=conn, table_name=test_table_name)

        prefix = "LIN"
        for i in range(2015550256, 2015550260):
            receipt_number = "{}{}".format(prefix, i)
            print(i)
            timestamp, title, message = uscis_check(receipt_number=receipt_number)
            print()
            await insert_entry(conn=conn, table_name=test_table_name,
                               case_number=receipt_number,
                               last_updated=timestamp,
                               current_status=title,
                               history=message)

        row = await get_all(conn=conn, table_name=test_table_name)
        for u in row:
            print(u)
        print(len(row))
    finally:
        await conn.close()

asyncio.get_event_loop().run_until_complete(main())
