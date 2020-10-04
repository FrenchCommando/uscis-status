import asyncio
from src.update_functions import update_entries, smart_update_all, refresh_status, refresh_selected_status


# asyncio.get_event_loop().run_until_complete(update_entries(
#     it=[],
#     skip_recent_threshold=1,
# ))

asyncio.get_event_loop().run_until_complete(update_entries(
    it=[f"LIN{2090318927 + i}" for i in range(1)],
    skip_recent_threshold=0,
))

# asyncio.get_event_loop().run_until_complete(smart_update_all(
#     prefix="LIN", date_start=20001, index_start=50001, skip_recent_threshold=1))
# asyncio.get_event_loop().run_until_complete(smart_update_all(
#     prefix="LIN", date_start=20900, index_start=1, skip_recent_threshold=1))
# #
asyncio.get_event_loop().run_until_complete(refresh_status(
    status='Case Was Approved And A Decision Notice Was Sent', skip_recent_threshold=0))
# asyncio.get_event_loop().run_until_complete(refresh_selected_status(
#     filter_function=lambda x: 0 < x < 100, skip_recent_threshold=1))
