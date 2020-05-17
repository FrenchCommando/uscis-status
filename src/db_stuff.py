import asyncio
import asyncpg
from src.constants import uscis_database, uscis_table_name
from src.db_secrets import postgres_user, postgres_password


async def connect_to_database(database):
    try:
        conn = await asyncpg.connect(
            user=postgres_user, password=postgres_password, database=database)
    except asyncpg.InvalidCatalogNameError:
        sys_conn = await asyncpg.connect(user=postgres_user)
        await sys_conn.execute(
            f'CREATE DATABASE "{database}" OWNER "{postgres_user}"'
        )
        await sys_conn.close()
        conn = await asyncpg.connect(user=postgres_user, database=database)
    return conn


async def build_table(conn, table_name):
    try:
        await conn.execute(f'''
            CREATE TABLE {table_name}(
                id serial PRIMARY KEY,
                case_number text,
                timestamp text,
                response_title text,
                response_message text
            )
        ''')
    except asyncpg.exceptions.DuplicateTableError:
        print(f"Table {table_name} already exists")
        pass


async def drop_table(conn, table_name):
    await conn.execute(f'''
        DROP TABLE IF EXISTS {table_name};
    ''')


async def main():
    conn = await connect_to_database(database=uscis_database)
    await drop_table(conn=conn, table_name=uscis_table_name)
    await build_table(conn=conn, table_name=uscis_table_name)

    # Insert a record into the created table.
    await conn.execute(f'''
        INSERT INTO {uscis_table_name}(case_number, timestamp, response_title, response_message) 
        VALUES($1, $2, $3, $4)
    ''', 'Alice', "efefefe", "Received", "Type2")

    # Select a row from the table.
    row = await conn.fetchrow(
        f'SELECT * FROM {uscis_table_name} WHERE case_number = $1', 'Bob')
    print(row)
    row2 = await conn.fetch(
        f'SELECT * FROM {uscis_table_name}')
    print(row2)
    print(len(row2))
    await conn.close()

asyncio.get_event_loop().run_until_complete(main())
