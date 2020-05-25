import asyncio
import aiohttp
from src.constants import localhost, port_number

server_path = localhost.format(port=port_number)


async def make_requests():
    async with aiohttp.ClientSession() as session:
        async with session.get(server_path) as resp:
            print(resp.status)
            print(await resp.text())
        rep = await session.post(server_path, data={"power": 10})
        print(rep)

loop = asyncio.get_event_loop()
loop.run_until_complete(make_requests())
loop.close()
