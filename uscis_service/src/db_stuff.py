import asyncpg
from src.db_secrets import postgres_user, postgres_password
from src.constants import pg_port_number, host
from src.db_def import table_to_specs


async def connect_to_database(database: str):
    try:
        pool = await asyncpg.create_pool(
            dsn=f"postgresql://{postgres_user}:{postgres_password}@{host}:{pg_port_number}/{database}",
        )
    except asyncpg.InvalidCatalogNameError:
        sys_conn = await asyncpg.connect(
            dsn=f"postgresql://{postgres_user}:{postgres_password}@{host}:{pg_port_number}"
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{database}" OWNER "{postgres_user}";'
        )
        await sys_conn.close()
        pool = await asyncpg.create_pool(
            dsn=f"postgresql://{postgres_user}:{postgres_password}@{host}:{pg_port_number}/{database}",
        )
    return pool


async def build_table(conn: asyncpg.Connection, table_name: str):
    table_filter_test = table_name.split("_", 1)[-1] if table_name.startswith("test") else table_name
    await conn.execute(f'CREATE TABLE IF NOT EXISTS {table_name}({table_to_specs[table_filter_test]});')


async def drop_table(conn: asyncpg.Connection, table_name: str):
    await conn.execute(f'DROP TABLE IF EXISTS {table_name};')


async def insert_entry(conn: asyncpg.Connection, table_name: str, **kwargs):
    await conn.execute(f'''
        INSERT INTO {table_name}({",".join(kwargs.keys())})
        VALUES({",".join(f"${i+1}" for i in range(len(kwargs.keys())))});
    ''', *kwargs.values())
    return "All good"


async def update_case(conn: asyncpg.Connection, table_name: str, case_number: str, **kwargs):
    await conn.execute(f'''
        UPDATE {table_name}
            SET {','.join(f'{k} = ${i}' for i, k in enumerate(kwargs.keys(), 1))}
            WHERE case_number = '{case_number}';
    ''', *kwargs.values())
    return "All good"


async def delete_case(conn: asyncpg.Connection, table_name: str, case_number: str):
    command = f'''
        DELETE FROM {table_name}
            WHERE case_number = '{case_number}';
    '''
    await conn.execute(command)
    return "All good"


async def get_all(conn: asyncpg.Connection, table_name: str, ignore_null: bool = False):
    if ignore_null:
        return await conn.fetch(f'SELECT * FROM {table_name} WHERE current_status IS NOT NULL;')
    return await conn.fetch(f'SELECT * FROM {table_name};')


async def get_all_case(conn: asyncpg.Connection, table_name: str, case_number: str):
    return await conn.fetch(f'SELECT * FROM {table_name} WHERE case_number = $1;', case_number)


async def get_all_status(conn: asyncpg.Connection, table_name: str, status: str):
    return await conn.fetch(f'SELECT * FROM {table_name} WHERE current_status = $1;', status)


async def get_attribute_from_case(conn: asyncpg.Connection, table_name: str, case_number: str, attribute: str):
    return await conn.fetch(f'SELECT {attribute} FROM {table_name} WHERE case_number = $1;', case_number)
