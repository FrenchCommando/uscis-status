import aiohttp
import asyncio
import gc
import sys
from aiohttp import web
from collections import defaultdict
import datetime as dt
from src.constants import port_number
from src.db_analysis_functions import count_date_status_function, count_date_status_format, \
    count_approval_history_function, get_form_date
from src.db_interaction import init_tables, \
    get_all_uscis, get_all_case_uscis, get_all_status_uscis, get_pool, get_all_errors
from src.message_stuff import status_to_msg
from src.update_functions import update_case_internal


async def handle_case(request):
    pool = request.app['pool']
    receipt_number = request.match_info.get('receipt_number', '')
    async with pool.acquire() as connection:
        async with aiohttp.ClientSession() as session:
            await update_case_internal(
                conn=connection, url_session=session,
                receipt_number=receipt_number,
                skip_recent_threshold=0,
            )
        rep = await get_all_case_uscis(conn=connection, case_number=receipt_number)
        rep_text = "\n".join([str(len(rep)), "\n".join(str(u) for u in rep)])
        return web.Response(text=rep_text)


async def handle_analysis(request):
    pool = request.app['pool']
    async with pool.acquire() as connection:
        records = await count_date_status_function(conn=connection)
        text = count_date_status_format(records=records)
        return web.Response(text=text)


async def handle_approval_analysis(request):
    pool = request.app['pool']
    form = request.match_info.get('form', '129')
    date_str = request.match_info.get('date', '')
    date = dt.datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else dt.datetime.now().date()
    async with pool.acquire() as connection:
        records = await count_approval_history_function(conn=connection, form=form, date=date)
        text = count_date_status_format(records=records)
        return web.Response(text=text)


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

        def get_line(u):
            case_value = u['case_number']
            status_value = u['current_status']
            args_value = u['current_args']
            form_value, date_value = get_form_date(
                current_status=status_value, current_args=args_value
            )
            date_str = date_value.strftime("%Y-%m-%d") if date_value else date_value
            return f"{case_value}\t{status_value}\t{form_value}\t{date_str}"

        rep_text = "\n".join([str(len(rep)), "\n".join(get_line(u=u) for u in rep)])
        return web.Response(text=rep_text)


async def handle_main(request):
    pool = request.app['pool']
    async with pool.acquire() as connection:
        print("Pre-Pull all uscis data")
        rep = await get_all_uscis(conn=connection)

        size_rep = f"Pre - Size of Pulled Data:\t{sys.getsizeof(rep)}\n"
        print(size_rep)

        text = [f"Number of entries {len(rep)}", ""]

        status_number = defaultdict(int)
        for line in rep:
            current_status = line["current_status"]
            status_number[current_status] += 1

        for status, length in sorted(status_number.items(), key=lambda k: k[1], reverse=True):
            if length:
                text.append(f"Number of entries for {status}: {length}")

        text.append("")
        errors = await get_all_errors(conn=connection)
        for u in errors:
            text.append(str(u))
        text.append("")
        text.append(str(len(errors)))
        text.append("")

        size_text = \
            f"Size of Pulled Data:\t{sys.getsizeof(rep)}\n" \
            f"Size of Output Text;\t{sys.getsizeof(text)}"
        print(size_text)

        text.append(f"\n{size_text}")
        gc.collect()
        return web.Response(text="\n".join(text))


async def init_app():
    """Initialize the application server."""
    app_inst = web.Application()
    app_inst['pool'] = await get_pool()

    async with app_inst['pool'].acquire() as connection:
        await init_tables(conn=connection)

    app_inst.router.add_route('GET', '/case/{receipt_number}', handle_case)
    app_inst.router.add_route('GET', '/status/{status}', handle_status)
    app_inst.router.add_route('GET', '/analysis', handle_analysis)
    app_inst.router.add_route('GET', '/approval_analysis/{form}/{date}', handle_approval_analysis)
    app_inst.router.add_route('GET', '/all', handle_all)
    app_inst.router.add_route('GET', '/', handle_main)
    return app_inst


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, port=port_number)
