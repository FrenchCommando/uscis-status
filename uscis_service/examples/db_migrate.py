import asyncio
import asyncpg
import datetime
from src.db_stuff import drop_table, build_table, insert_entry, get_all, connect_to_database, read_db
from src.constants import uscis_database, uscis_table_name
from src.db_def import table_to_specs


temp_table_name = "temp_table_name"
table_to_specs[temp_table_name] = \
    "case_number text PRIMARY KEY, " \
    "last_updated timestamp, " \
    "current_status text, " \
    "current_args text, " \
    "history text"


async def migrate_tables():
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            all_data = await get_all(conn=conn, table_name=uscis_table_name, ignore_null=True)
            one_line = all_data[0]
            print(one_line)
            d = one_line["last_updated"]
            timestamp = datetime.datetime.strptime(d, "%a, %d %b %Y %H:%M:%S %Z")
            print(timestamp)
            for u, v in one_line.items():
                print(u, v)

        async with pool.acquire() as conn:
            await build_table(conn=conn, table_name=temp_table_name)
            await read_db(conn=conn, table_name=temp_table_name, len_only=False, head=5)
            await read_db(conn=conn, table_name=uscis_table_name, len_only=False, head=5)

        async with pool.acquire() as conn:
            all_data = await get_all(conn=conn, table_name=uscis_table_name, ignore_null=True)
            for u in all_data:
                try:
                    d = dict(
                        case_number=u["case_number"],
                        last_updated=datetime.datetime.strptime(u["last_updated"], "%a, %d %b %Y %H:%M:%S %Z"),
                        current_status=u["current_status"],
                        current_args=u["current_args"],
                        history="",
                    )
                    await insert_entry(conn=conn, table_name=temp_table_name, **d)
                except ValueError:
                    continue
                except asyncpg.exceptions.UniqueViolationError:
                    continue
        print("Data is copied")

        async with pool.acquire() as conn:
            await read_db(conn=conn, table_name=temp_table_name, len_only=False, head=5)
            await read_db(conn=conn, table_name=uscis_table_name, len_only=False, head=5)

    finally:
        await pool.close()


async def move_tables():
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            await read_db(conn=conn, table_name=temp_table_name, len_only=False, head=5)
            await read_db(conn=conn, table_name=uscis_table_name, len_only=False, head=5)
            await drop_table(conn=conn, table_name=uscis_table_name)
            await build_table(conn=conn, table_name=uscis_table_name)

        async with pool.acquire() as conn:
            all_data = await get_all(conn=conn, table_name=temp_table_name, ignore_null=True)
            for u in all_data:
                try:
                    d = dict(
                        case_number=u["case_number"],
                        last_updated=u["last_updated"],
                        current_status=u["current_status"],
                        current_args=u["current_args"],
                        history="",
                    )
                    await insert_entry(conn=conn, table_name=uscis_table_name, **d)
                except ValueError:
                    continue
                except asyncpg.exceptions.UniqueViolationError:
                    continue
        print("Data is copied")

        async with pool.acquire() as conn:
            await read_db(conn=conn, table_name=temp_table_name, len_only=False, head=5)
            await read_db(conn=conn, table_name=uscis_table_name, len_only=False, head=5)

    finally:
        await pool.close()


async def drop_temp_table():
    pool = await connect_to_database(database=uscis_database)
    try:
        async with pool.acquire() as conn:
            await read_db(conn=conn, table_name=temp_table_name, len_only=False, head=5)
            await read_db(conn=conn, table_name=uscis_table_name, len_only=False, head=5)
            await drop_table(conn=conn, table_name=temp_table_name)

        print("Temp table deleted")

        async with pool.acquire() as conn:
            await read_db(conn=conn, table_name=uscis_table_name, len_only=False, head=5)

    finally:
        await pool.close()

# asyncio.get_event_loop().run_until_complete(migrate_tables())
# asyncio.get_event_loop().run_until_complete(move_tables())
# asyncio.get_event_loop().run_until_complete(drop_temp_table())
