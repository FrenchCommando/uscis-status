import asyncio
from src.update_functions import update_entries, smart_update_all, refresh_case, refresh_selected_status


# asyncio.get_event_loop().run_until_complete(update_entries(it=[]))

# asyncio.get_event_loop().run_until_complete(update_entries(it=[f"LIN{2015550250 + i}" for i in range(100)]))

# asyncio.get_event_loop().run_until_complete(smart_update_all(
#     prefix="LIN", date_start=20001, index_start=50001, skip_existing=False))
# asyncio.get_event_loop().run_until_complete(smart_update_all(
#     prefix="LIN", date_start=20902, index_start=1, skip_existing=False))

# asyncio.get_event_loop().run_until_complete(refresh_case(status='CASE STATUS'))
# asyncio.get_event_loop().run_until_complete(refresh_selected_status(filter_function=lambda x: 0 < x < 100))
