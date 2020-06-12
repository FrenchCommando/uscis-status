import aiohttp
import asyncio
from src.message_stuff import get_arguments_from_string, args_to_string
from src.parse_site import check as uscis_check


async def main():
    prefix = "LIN"
    i = 2090097008

    async with aiohttp.ClientSession() as session:
        for ii in range(1):
            receipt_number = "{}{}".format(prefix, i + ii)
            timestamp, title, message = await uscis_check(receipt_number=receipt_number, url_session=session)
            current_args = args_to_string(d=get_arguments_from_string(s=message, status=title))
            print(f"{receipt_number}\t{timestamp}\t{title}\n\t{message}\n\t{current_args}")


asyncio.get_event_loop().run_until_complete(main())
