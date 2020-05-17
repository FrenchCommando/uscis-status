import asyncio
from aiohttp import web
from src.db_pool_stuff import init_app

loop = asyncio.get_event_loop()
app = loop.run_until_complete(init_app())
web.run_app(app, port=8808)
