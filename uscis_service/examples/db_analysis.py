import asyncio
from src.db_analysis_functions import summary_analysis
from src.message_stuff import string_to_args


# asyncio.get_event_loop().run_until_complete(summary_analysis(print_results=True))


def select_form(line):
    current_args = line["current_args"]
    d = string_to_args(s=current_args)
    form_name = d.get('form_long_name', "")
    ref = "Form I-129, Petition for a Nonimmigrant Worker"
    return form_name == ref


asyncio.get_event_loop().run_until_complete(summary_analysis(custom_filter=select_form, print_results=True))
