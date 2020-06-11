import asyncio
from src.update_functions import refresh_error, delete_entries


asyncio.get_event_loop().run_until_complete(refresh_error())
# asyncio.get_event_loop().run_until_complete(delete_entries(["LIN2090133946", "LIN2090203249"]))
