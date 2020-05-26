import asyncio
from src.update_functions import update_entries, delete_entries


start_index = 2020050000
l_i = range(start_index, start_index + 50)
ll = [f"LIN{i}" for i in l_i]
# asyncio.get_event_loop().run_until_complete(delete_entries(it=ll))
asyncio.get_event_loop().run_until_complete(update_entries(it=ll))
