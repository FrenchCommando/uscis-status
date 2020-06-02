import aiohttp
import asyncio
from uscis_service.src.parse_site import check as uscis_check


async def main():
    prefix = "LIN"
    i = 2015550256

    async with aiohttp.ClientSession() as session:
        for i in range(2015550256, 2015550656):
            receipt_number = "{}{}".format(prefix, i)
            print(await uscis_check(receipt_number=receipt_number, url_session=session))


asyncio.get_event_loop().run_until_complete(main())