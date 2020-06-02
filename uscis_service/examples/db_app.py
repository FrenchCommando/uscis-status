from aiohttp import web
from examples.db_server import handle_case, handle_status, handle_all, handle_main
from src.db_interaction import get_pool

app_inst = web.Application()
app_inst['pool'] = await get_pool()

app_inst.router.add_route('GET', '/case/{receipt_number}', handle_case)
app_inst.router.add_route('GET', '/status/{status}', handle_status)
app_inst.router.add_route('GET', '/all', handle_all)
app_inst.router.add_route('GET', '/', handle_main)
