import aiohttp
import asyncio
from src.parse_site import check as uscis_check


async def main():
    prefix = "LIN"
    i = 2015550256

    async with aiohttp.ClientSession() as session:
        for ii in range(1000):
            receipt_number = "{}{}".format(prefix, i + ii)
            print(receipt_number, await uscis_check(receipt_number=receipt_number, url_session=session))


asyncio.get_event_loop().run_until_complete(main())
