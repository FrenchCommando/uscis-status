import asyncio
from src.update_functions import update_entries, smart_update_all, \
    refresh_error, refresh_case, refresh_selected_status

start_index = 2010050354
l_i = range(start_index, start_index + 100)
ll = [f"LIN{i}" for i in l_i]
# asyncio.get_event_loop().run_until_complete(update_entries(it=ll))
# asyncio.get_event_loop().run_until_complete(update_entries(it=[]))

# asyncio.get_event_loop().run_until_complete(smart_update_all(
#     prefix="LIN", date_start=20001, index_start=50001, skip_existing=False, chunk_size=100,
# ))
asyncio.get_event_loop().run_until_complete(smart_update_all(
    prefix="LIN", date_start=20902, index_start=1, skip_existing=False, chunk_size=100,
))

asyncio.get_event_loop().run_until_complete(refresh_case(status='CASE STATUS'))
# asyncio.get_event_loop().run_until_complete(refresh_selected_status(filter_function=lambda x: 100 < x < 500))
