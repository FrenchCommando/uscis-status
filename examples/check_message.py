from src.message_stuff import *


v_s = """On April 7, 2020, we received your Form I-765, Application for Employment Authorization, Receipt Number LIN2015550257, and sent you the receipt notice that describes how we will process your case.  Please follow the instructions in the notice.  If you do not receive your receipt notice by May 7, 2020, contact the USCIS Contact Center at \t<a href="https://www.uscis.gov/contactcenter" target="_blank">www.uscis.gov/contactcenter</a>\t.  If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t to give us your new mailing address."""
v_case = "Case Was Received"
v_d = get_arguments_from_string(s=v_s, status=v_case)
print(v_d)
s_d = args_to_string(d=v_d)
print(s_d)
s_back = string_to_args(s=s_d)
print(s_back)

print("Case Was Received",
      status_to_msg["Case Was Received"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
        notice_deadline="April 7, 2020",
      ))

print("Case Was Approved",
      status_to_msg["Case Was Approved"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
        notice_deadline="April 7, 2020",
      ))

print("Card Was Delivered To Me By The Post Office",
      status_to_msg["Card Was Delivered To Me By The Post Office"].format(
        date="April 1, 2020",
        receipt_number="LIN45435435",
        tracking_number="019490328490289043",
      ))

print("Name Was Updated",
      status_to_msg["Name Was Updated"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
      ))

print("Request for Additional Evidence Was Sent",
      status_to_msg["Request for Additional Evidence Was Sent"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
        notice_deadline="April 7, 2020",
      ))

print("Notice Explaining USCIS Actions Was Mailed",
      status_to_msg["Notice Explaining USCIS Actions Was Mailed"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
        notice_deadline="April 7, 2020",
      ))

print("Notice Was Returned To USCIS Because The Post Office Could Not Deliver It",
      status_to_msg["Notice Was Returned To USCIS Because The Post Office Could Not Deliver It"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
        notice_deadline="April 7, 2020",
      ))

print("Withdrawal Acknowledgement Notice Was Sent",
      status_to_msg["Withdrawal Acknowledgement Notice Was Sent"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
        notice_deadline="April 7, 2020",
      ))

print("Response To USCIS' Request For Evidence Was Received",
      status_to_msg["Response To USCIS' Request For Evidence Was Received"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
        notice_deadline="April 7, 2020",
      ))

print("Fee Will Be Refunded",
      status_to_msg["Fee Will Be Refunded"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
        notice_deadline="April 7, 2020",
      ))

print("Case Was Rejected Because It Was Improperly Filed",
      status_to_msg["Case Was Rejected Because It Was Improperly Filed"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
        notice_deadline="April 7, 2020",
      ))
print("Case Transferred And New Office Has Jurisdiction",
      status_to_msg["Case Transferred And New Office Has Jurisdiction"].format(
        date="April 1, 2020",
        form_long_name="long_name",
        receipt_number="LIN45435435",
        notice_deadline="April 7, 2020",
      ))
print("Case Was Sent To The Department of State",
      status_to_msg["Case Was Sent To The Department of State"].format(
        date="April 1, 2020",
        receipt_number="LIN45435435",
      ))
