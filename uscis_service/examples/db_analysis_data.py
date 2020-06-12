import asyncio
from src.db_analysis_functions import count_date_status


asyncio.get_event_loop().run_until_complete(count_date_status())
