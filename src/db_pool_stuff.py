import asyncio
import asyncpg
from aiohttp import web
from src.db_secrets import postgres_user, postgres_password


async def handle(request):
    """Handle incoming requests."""
    pool = request.app['pool']
    power = int(request.match_info.get('power', 10))

    # Take a connection from the pool.
    async with pool.acquire() as connection:
        # Open a transaction.
        async with connection.transaction():
            # Run the query passing the request argument.
            result = await connection.fetchval('select 2 ^ $1', power)
            return web.Response(
                text="2 ^ {} is {}".format(power, result))


async def init_app():
    """Initialize the application server."""
    app_inst = web.Application()
    # Create a database connection pool
    app_inst['pool'] = await asyncpg.create_pool(
        user=postgres_user, password=postgres_password
    )
    # Configure service routes
    app_inst.router.add_route('GET', '/{power:\d+}', handle)
    app_inst.router.add_route('GET', '/', handle)
    return app_inst


loop = asyncio.get_event_loop()
app = loop.run_until_complete(init_app())
web.run_app(app)
