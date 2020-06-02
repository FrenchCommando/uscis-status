from uscis_service.src.db_stuff import get_all, get_all_case, get_all_status, connect_to_database
from uscis_service.src.constants import uscis_table_name, uscis_database


async def get_pool():
    return await connect_to_database(database=uscis_database)


async def get_all_uscis(conn):
    return await get_all(conn=conn, table_name=uscis_table_name)


async def get_all_case_uscis(conn, case_number):
    return await get_all_case(conn=conn, table_name=uscis_table_name, case_number=case_number)


async def get_all_status_uscis(conn, status):
    return await get_all_status(conn=conn, table_name=uscis_table_name, status=status)
