import asyncio
from src.db_analysis_functions import summary_analysis, filter_receipt, filter_status, filter_form


asyncio.get_event_loop().run_until_complete(
    summary_analysis(print_results=True, buckets_instead_of_strip=True))

asyncio.get_event_loop().run_until_complete(
    summary_analysis(custom_filter=filter_form(ref="Form I-129, Petition for a Nonimmigrant Worker"),
                     print_results=True, buckets_instead_of_strip=True))


asyncio.get_event_loop().run_until_complete(
    summary_analysis(custom_filter=filter_status(ref="CASE STATUS"),
                     print_results=False, buckets_instead_of_strip=False))

asyncio.get_event_loop().run_until_complete(
    summary_analysis(custom_filter=filter_receipt(ref=r"LIN2000\d+"),
                     print_results=True, buckets_instead_of_strip=True))
