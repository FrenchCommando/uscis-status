import asyncio
import datetime as dt
from src.db_analysis_functions import count_date_status, count_approval_history


# asyncio.get_event_loop().run_until_complete(count_date_status())
asyncio.get_event_loop().run_until_complete(
    count_approval_history(form="I-129", date=dt.date(year=2020, month=6, day=11)))
