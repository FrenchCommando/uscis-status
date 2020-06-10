import asyncio
from src.update_functions import refresh_error


asyncio.get_event_loop().run_until_complete(refresh_error())
