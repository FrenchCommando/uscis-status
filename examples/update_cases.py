import asyncio
from src.update_functions import update_entries, delete_entries, smart_update_all, refresh_case, refresh_error


start_index = 2006950236
l_i = range(start_index, start_index + 10)
ll = [f"LIN{i}" for i in l_i]
# asyncio.get_event_loop().run_until_complete(update_entries(it=ll))
# asyncio.get_event_loop().run_until_complete(update_entries(it=[]))

asyncio.get_event_loop().run_until_complete(smart_update_all(
    prefix="LIN", date_start=20001, index_start=50001, skip_existing=True, chunk_size=50,
))

# asyncio.get_event_loop().run_until_complete(refresh_case(status='Fingerprint Fee Was Received'))
# asyncio.get_event_loop().run_until_complete(refresh_error())

# need one function to clean end of queues that should have been None and were misattributed - nah just refresh
