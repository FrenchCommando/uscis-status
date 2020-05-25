import asyncio
from aiohttp import web
from src.constants import port_number
from sandbox.db_pool_stuff import init_app

loop = asyncio.get_event_loop()
app = loop.run_until_complete(init_app())
web.run_app(app, port=port_number)
