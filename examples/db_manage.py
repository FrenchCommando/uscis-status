import asyncio
from src.constants import uscis_database, uscis_table_name
from src.db_stuff import connect_to_database, drop_table, build_table, insert_entry, get_all, get_all_case


async def main():
    conn = await connect_to_database(database=uscis_database)
    try:
        # await drop_table(conn=conn, table_name=uscis_table_name)
        await build_table(conn=conn, table_name=uscis_table_name)

        await insert_entry(conn=conn, table_name=uscis_table_name,
                           case_number="Alice",
                           timestamp="2020",
                           response_title="received",
                           response_message="received_message")
        await insert_entry(conn=conn, table_name=uscis_table_name,
                           case_number="Bob",
                           timestamp="20200202",
                           response_title="received2",
                           response_message="received_message")

        # Select a row from the table.
        row = await get_all_case(conn=conn, table_name=uscis_table_name, case_number="Alice")
        print(row)
        row2 = await get_all(conn=conn, table_name=uscis_table_name)
        print(row2)
        print(len(row2))
    finally:
        await conn.close()

asyncio.get_event_loop().run_until_complete(main())
