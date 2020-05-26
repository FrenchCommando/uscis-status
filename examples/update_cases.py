import asyncio
from src.update_functions import update_entries, delete_entries


l_i = [
    2015550567,  # Fee Will Be Refunded
    2015550574,  # Case Was Rejected Because It Was Improperly Filed
    2015550575,  # Case Was Rejected Because It Was Improperly Filed
    2015550001,  # Case Transferred And New Office Has Jurisdiction
    2015550002,  # Case Transferred And New Office Has Jurisdiction
    2015550085,  # Case Was Sent To The Department of State
    2015550025,  # Card Was Picked Up By The United States Postal Service
    2015550037,  # Case Rejected Because The Version Of The Form I Sent Is No Longer Accepted
    2015550095,  # Fees Were Waived
    2015550110,  # Case Was Rejected Because I Did Not Sign My Form
    2015550118,  # Card Was Mailed To Me
    2015550139,  # Case Was Updated To Show Fingerprints Were Taken
    2015550155,  # New Card Is Being Produced
    2015550236,  # Card Is Being Returned to USCIS by Post Office
]
ll = [f"LIN{i}" for i in l_i]
# asyncio.get_event_loop().run_until_complete(delete_entries(it=ll))
asyncio.get_event_loop().run_until_complete(update_entries(it=ll))
