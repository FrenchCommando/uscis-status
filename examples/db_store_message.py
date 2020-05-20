import asyncio
from src.constants import uscis_database, uscis_table_name
from src.db_stuff import connect_to_database, drop_table, build_table, insert_entry, \
    get_all, get_all_case
from src.parse_site import UscisInterface


interface = UscisInterface()


async def async_range(start, end):
    for i in range(start, end):
        yield i


async def main():
    conn = await connect_to_database(database=uscis_database)
    try:
        await drop_table(conn=conn, table_name=uscis_table_name)
        await build_table(conn=conn, table_name=uscis_table_name)

        prefix = "LIN"
        async for i in async_range(2015550256, 2015550260):
            receipt_number = "{}{}".format(prefix, i)
            timestamp, title, message = await interface.check(receipt_number=receipt_number)

            await insert_entry(conn=conn, table_name=uscis_table_name,
                               case_number=receipt_number,
                               timestamp=timestamp,
                               response_title=title,
                               response_message=message)

        row = await get_all(conn=conn, table_name=uscis_table_name)
        print(row)
        print(len(row))
    finally:
        await conn.close()

asyncio.get_event_loop().run_until_complete(main())
