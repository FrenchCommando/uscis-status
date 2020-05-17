import asyncio
import aiohttp


async def make_requests():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8808') as resp:
            print(resp.status)
            print(await resp.text())
        rep = await session.post('http://localhost:8808', data=b'data')
        print(rep)

loop = asyncio.get_event_loop()
loop.run_until_complete(make_requests())
loop.close()
