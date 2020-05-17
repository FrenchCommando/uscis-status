import asyncpg
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


async def insert_entry(conn, table_name, case_number, timestamp, response_title, response_message):
    await conn.execute(f'''
        INSERT INTO {table_name}(case_number, timestamp, response_title, response_message) 
        VALUES($1, $2, $3, $4)
    ''', case_number, timestamp, response_title, response_message)
    return "All good"


async def get_all(conn, table_name):
    return await conn.fetch(f'SELECT * FROM {table_name}')


async def get_all_case(conn, table_name, case_number):
    return await conn.fetch(f'SELECT * FROM {table_name} WHERE case_number = $1', case_number)
