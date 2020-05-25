import asyncpg
from aiohttp import web
from src.constants import uscis_database, uscis_table_name
from src.db_secrets import postgres_user, postgres_password
from src.db_stuff import get_all_case, get_all, insert_entry, build_table


async def handle_power(request):
    """Handle incoming requests."""
    pool = request.app['pool']
    power = int(request.match_info.get('power', 10))
    async with pool.acquire() as connection:
        async with connection.transaction():
            rep = await insert_entry(
                conn=connection,
                table_name=uscis_table_name,
                case_number="LIN12312",
                timestamp="202020202",
                response_title="accepted",
                response_message="accepted_message")
            return web.Response(text=rep)


async def handle_case(request):
    power = request.match_info.get('case_number', "default_number")
    return web.Response(
        text="2 ^ {} is {}".format(power, power))


async def handle(request):
    return web.Response(text="Nothing to do")


async def init_app():
    """Initialize the application server."""
    app_inst = web.Application()
    app_inst['pool'] = await asyncpg.create_pool(
        user=postgres_user, password=postgres_password, database=uscis_database
    )

    async with app_inst['pool'].acquire() as connection:
        async with connection.transaction():
            await build_table(conn=connection, table_name=uscis_table_name)

    app_inst.router.add_route('POST', '/{power:\d+}', handle_power)
    app_inst.router.add_route('GET', '/{case_number}', handle_case)
    app_inst.router.add_route('GET', '/', handle)
    return app_inst
