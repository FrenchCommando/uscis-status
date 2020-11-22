import aiohttp
import asyncio
import sys
from aiohttp import web
from collections import defaultdict, Counter
import datetime as dt
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

        rep_text = "\n".join([str(len(rep)),
                              "\n".join(get_line(u=u)
                                        for u in sorted(rep, key=lambda u: u['case_number'])[:-1000:-1])])
        return web.Response(text=rep_text)


async def response_counter(request, line_to_item):
    pool = request.app['pool']
    async with pool.acquire() as connection:
        rep = await get_all_uscis(conn=connection)

        text = [f"Number of entries {len(rep)}", ""]

        item_number = Counter()
        for line in rep:
            item = line_to_item(line=line)
            item_number[item] += 1

        for status, length in item_number.most_common():
            if length:
                text.append(f"Number of entries :\t{length:7d}\t\t{status}")

        text.append("")
        errors = await get_all_errors(conn=connection)
        for u in errors:
            text.append(str(u))
        text.append("")
        text.append(str(len(errors)))
        text.append("")

        size_text = \
            f"Size of Pulled Data:\t{sys.getsizeof(rep)}\n" \
            f"Size of Output Text:\t{sys.getsizeof(text)}\n" \
            f"Head of message:\t{text[:10]}\n" \
            f"Tail of message:\t{text[-10:]}"

        text.append(f"\n{size_text}")

        if len(text) < 1e5:
            return web.Response(text="\n".join(text))
        return web.Response(text="\n".join(["I'm a very short text", size_text]))


async def handle_form(request):
    def get_form(line):
        status_value = line['current_status']
        args_value = line['current_args']
        form_value, date_value = get_form_date(
            current_status=status_value, current_args=args_value
        )
        return form_value
    return await response_counter(request=request, line_to_item=get_form)


async def handle_main(request):
    return await response_counter(request=request, line_to_item=lambda line: line["current_status"])


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
    app_inst.router.add_route('GET', '/form', handle_form)
    app_inst.router.add_route('GET', '/', handle_main)
    return app_inst


if __name__ == "__main__":
    from src.constants import port_number
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, port=port_number)
