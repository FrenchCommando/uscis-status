import asyncio
from src.constants import uscis_database, uscis_table_name
from src.db_stuff import connect_to_database, drop_table, build_table, insert_entry, \
    get_all, get_all_case


async def main():
    conn = await connect_to_database(database=uscis_database)
    test_table_name = f"test_{uscis_table_name}"
    try:
        await drop_table(conn=conn, table_name=test_table_name)
        await build_table(conn=conn, table_name=test_table_name)

        await insert_entry(conn=conn, table_name=test_table_name,
                           case_number="Alice",
                           last_updated="2020",
                           current_status="received",
                           history="received_message")
        await insert_entry(conn=conn, table_name=test_table_name,
                           case_number="Bob",
                           last_updated="20200202",
                           current_status="received2",
                           history="received_message")
        await insert_entry(
            conn=conn, table_name=test_table_name,
            case_number="Charles",
            last_updated="202000000202",
            current_status="received3",
            history="received_message3")

        # Select a row from the table.
        row = await get_all_case(conn=conn, table_name=test_table_name, case_number="Alice")
        print(row)
        row2 = await get_all(conn=conn, table_name=test_table_name)
        print(row2)
        print(len(row2))
    finally:
        await conn.close()

asyncio.get_event_loop().run_until_complete(main())
