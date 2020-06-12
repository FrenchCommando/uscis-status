import asyncio
from src.db_analysis_functions import summary_analysis, summary_analysis_form, summary_analysis_status


asyncio.get_event_loop().run_until_complete(summary_analysis(print_results=True))
asyncio.get_event_loop().run_until_complete(summary_analysis_form(
    ref_form="Form I-129, Petition for a Nonimmigrant Worker",
    print_results=True, buckets_instead_of_strip=True))
asyncio.get_event_loop().run_until_complete(summary_analysis_status(
    ref_status="CASE STATUS",
    print_results=False, buckets_instead_of_strip=False))
