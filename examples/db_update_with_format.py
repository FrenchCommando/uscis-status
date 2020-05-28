import asyncio
from src.constants import uscis_database, uscis_table_name
from src.db_stuff import connect_to_database, drop_table, build_table, insert_entry, \
    get_all, get_all_case, update_case
from src.message_stuff import string_to_args, get_arguments_from_string, rebuild_string_from_template, \
    args_to_string, remove_tags
from src.parse_site import check as uscis_check


async def main():
    conn = await connect_to_database(database=uscis_database)
    test_table_name = f"test_{uscis_table_name}"
    try:
        await drop_table(conn=conn, table_name=test_table_name)
        await build_table(conn=conn, table_name=test_table_name)

        async def update_case_internal(receipt_number):
            rep = await get_all_case(conn=conn, table_name=test_table_name, case_number=receipt_number)
            timestamp, title, message = uscis_check(receipt_number=receipt_number)
            if rep:
                print(rep)
                current_args = args_to_string(d=get_arguments_from_string(s=message, status=title))
                old_status = rep[0]['current_status']
                old_args = rep[0]['current_args']
                old_history = rep[0]['history']
                if (old_status, old_args) == (title, current_args):
                    new_history_joined = old_history
                else:
                    new_history = ":".join([title, current_args])
                    new_history_joined = "||".join([new_history, old_history]) if old_history else new_history
                rep2 = await update_case(conn=conn, table_name=test_table_name, case_number=receipt_number,
                                         last_updated=timestamp,
                                         current_status=title,
                                         current_args=current_args,
                                         history=new_history_joined
                                         )
                print(rep2)
            else:
                print()
                current_args = args_to_string(d=get_arguments_from_string(s=message, status=title))
                if title is not None:
                    print(remove_tags(s=message) ==
                          rebuild_string_from_template(status=title, **string_to_args(s=current_args)))

                await insert_entry(conn=conn, table_name=test_table_name,
                                   case_number=receipt_number,
                                   last_updated=timestamp,
                                   current_status=title,
                                   current_args=current_args,
                                   history="")

        async def read_db():
            row = await get_all(conn=conn, table_name=test_table_name)
            for u in row:
                print(u)
            print(len(row))

        prefix = "LIN"

        async def test_number(number):
            print(number)
            await update_case_internal(receipt_number=f"{prefix}{number}")
            await read_db()
            print()

        for i in [  # just realized this list will be obsolete
            # 2015550361,  # Case Was Received
            # 2015550363,  # Case Was Received
            # 2015550362,  # Case Was Approved
            # 2015550364,  # Case Was Approved
            # 2015550360,  # Request for Additional Evidence Was Sent
            # 2015550064,  # Request for Additional Evidence Was Sent
            # 2015550361,  # Case Was Received - re
            # 2015550259,  # Card Was Delivered To Me By The Post Office
            # 2015550256,  # Name Was Updated
            # 2015550331,  # Name Was Updated
            # 2015550284,  # Notice Explaining USCIS Actions Was Mailed
            # 2015550336,  # Notice Was Returned To USCIS Because The Post Office Could Not Deliver It
            # 2015550503,  # Withdrawal Acknowledgement Notice Was Sent
            # 2015550507,  # Response To USCIS' Request For Evidence Was Received
            # 2015550507,  # Response To USCIS' Request For Evidence Was Received - how to escape the '
            # 2015550567,  # Fee Will Be Refunded
            # 2015550574,  # Case Was Rejected Because It Was Improperly Filed
            # 2015550575,  # Case Was Rejected Because It Was Improperly Filed
            # 2015550001,  # Case Transferred And New Office Has Jurisdiction
            # 2015550002,  # Case Transferred And New Office Has Jurisdiction
            # 2015550085,  # Case Was Sent To The Department of State
            # 2015550025,  # Card Was Picked Up By The United States Postal Service
            # 2015550037,  # Case Rejected Because The Version Of The Form I Sent Is No Longer Accepted
            # 2015550095,  # Fees Were Waived
            # 2015550110,  # Case Was Rejected Because I Did Not Sign My Form
            # 2015550118,  # Card Was Mailed To Me
            # 2015550139,  # Case Was Updated To Show Fingerprints Were Taken
            # 2015550155,  # New Card Is Being Produced
            # 2015550236,  # Card Is Being Returned to USCIS by Post Office
            # 2015650015,  # Date of Birth Was Updated
            # 2015650603,  # Form G-28 Was Rejected Because It Was Improperly Filed
            # 2015750588,  # Case Rejected Because I Sent An Incorrect Fee
            # 1900250001,  # Fingerprint Fee Was Received
            # 2000150095,  # Card Was Mailed To Me
            # 2000150163,  # Card Was Destroyed
            # 2000150282,  # Case Was Approved And My Decision Was Emailed
            # 2000350149,  # Case Was Denied
            # 2000350167,  # Card Was Returned To USCIS
            # 2000350256,  # Revocation Notice Was Sent
            # 2000350478,  # Case Was Transferred And A New Office Has Jurisdiction
            # 2000350654,  # Case is Ready to Be Scheduled for An Interview
            # 2000350658,  # Department of State Sent Case to USCIS For Review
            # 2000350671,  # Interview Cancelled
            # 2000350680,  # Expedite Request Denied
            # 2000350744,  # Interview Cancelled And Notice Ordered
            # 2015150141,  # Petition/Application Was Rejected For Insufficient Funds
            # 2015250040,  # Case Is On Hold Because Of Pending Litigation
            # 2000150375,  # Case Accepted By The USCIS Lockbox
            # 2015150303,  # Duplicate Notice Was Mailed
            # 2000350805,  # Duplicate Notice Was Mailed
            # 2000150723,  # Case Closed Benefit Received By Other Means
            2000150812,  # Case Was Automatically Revoked
            2000151044,  # Case Was Reopened
            9999999999,  # None
        ]:
            await test_number(number=i)

    finally:
        await conn.close()

asyncio.get_event_loop().run_until_complete(main())
