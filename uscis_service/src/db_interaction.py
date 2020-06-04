from src.db_stuff import get_all, get_all_case, get_all_status, connect_to_database, build_table
from src.constants import uscis_table_name, uscis_database, error_table_name


async def get_pool():
    return await connect_to_database(database=uscis_database)


async def get_all_uscis(conn):
    await build_table(conn=conn, table_name=uscis_table_name)
    await build_table(conn=conn, table_name=error_table_name)
    return await get_all(conn=conn, table_name=uscis_table_name, ignore_null=True)


async def get_all_case_uscis(conn, case_number):
    await build_table(conn=conn, table_name=uscis_table_name)
    await build_table(conn=conn, table_name=error_table_name)
    return await get_all_case(conn=conn, table_name=uscis_table_name, case_number=case_number)


async def get_all_status_uscis(conn, status):
    await build_table(conn=conn, table_name=uscis_table_name)
    await build_table(conn=conn, table_name=error_table_name)
    return await get_all_status(conn=conn, table_name=uscis_table_name, status=status)


async def get_all_errors(conn):
    await build_table(conn=conn, table_name=error_table_name)
    return await get_all(conn=conn, table_name=error_table_name)
