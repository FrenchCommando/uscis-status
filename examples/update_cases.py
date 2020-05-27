import asyncio
from src.update_functions import update_entries, delete_entries, smart_update_all, refresh_case


# start_index = 2020050000
# l_i = range(start_index, start_index + 50)
# ll = [f"LIN{i}" for i in l_i]
# asyncio.get_event_loop().run_until_complete(delete_entries(it=ll))
# asyncio.get_event_loop().run_until_complete(update_entries(it=ll))

# asyncio.get_event_loop().run_until_complete(smart_update_all(prefix="LIN", date_start=20001, index_start=50095))

asyncio.get_event_loop().run_until_complete(refresh_case(status='Name Was Updated', delete=False))
