import asyncio
from aiohttp import web
from src.constants import port_number
from src.db_interaction import get_all_uscis, get_all_case_uscis, get_all_status_uscis, get_pool
from src.message_stuff import status_to_msg


async def handle_case(request):
    pool = request.app['pool']
    receipt_number = request.match_info.get('receipt_number', '')
    async with pool.acquire() as connection:
        rep = await get_all_case_uscis(conn=connection, case_number=receipt_number)
        rep_text = "\n".join([str(len(rep)), "\n".join(str(u) for u in rep)])
        return web.Response(text=rep_text)


async def handle_status(request):
    pool = request.app['pool']
    status = request.match_info.get('status', '')
    async with pool.acquire() as connection:
        rep = await get_all_status_uscis(conn=connection, status=status)
        rep_text = "\n".join([str(len(rep)), "\n".join(str(u) for u in rep)])
        return web.Response(text=rep_text)


async def handle_all(request):
    pool = request.app['pool']
    async with pool.acquire() as connection:
        rep = await get_all_uscis(conn=connection)
        rep_text = "\n".join([str(len(rep)), "\n".join(str(u['case_number']) for u in rep)])
        return web.Response(text=rep_text)


async def handle_main(request):
    pool = request.app['pool']
    async with pool.acquire() as connection:
        rep = await get_all_uscis(conn=connection)
        text = [f"Number of entries {len(rep)}"]
        for status in status_to_msg:
            rep = await get_all_status_uscis(conn=connection, status=status)
            text.append(f"Number of entries for {status}: {len(rep)}")
        return web.Response(text="\n".join(text))


async def init_app():
    """Initialize the application server."""
    app_inst = web.Application()
    app_inst['pool'] = await get_pool()

    app_inst.router.add_route('GET', '/case/{receipt_number}', handle_case)
    app_inst.router.add_route('GET', '/status/{status}', handle_status)
    app_inst.router.add_route('GET', '/all', handle_all)
    app_inst.router.add_route('GET', '/', handle_main)
    return app_inst


loop = asyncio.get_event_loop()
app = loop.run_until_complete(init_app())
web.run_app(app, port=port_number)
