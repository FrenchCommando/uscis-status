import re


status_to_msg = {
    "Case Was Received": """On {date}, we received your {form_long_name}, Receipt Number {receipt_number}, and sent you the receipt notice that describes how we will process your case.  Please follow the instructions in the notice.  If you do not receive your receipt notice by {notice_deadline}, contact the USCIS Contact Center at \t<a href="https://www.uscis.gov/contactcenter" target="_blank">www.uscis.gov/contactcenter</a>\t.  If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t to give us your new mailing address.""",
    "Case Was Approved": """On {date}, we approved your {form_long_name}, Receipt Number {receipt_number}.  We sent you an approval notice.  Please follow the instructions in the notice. If you do not receive your approval notice by {notice_deadline}, please go to \t<a href="https://egov.uscis.gov/e-Request/Intro.do" target="_blank">www.uscis.gov/e-request</a>\t.  If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t  to give us your new mailing address.  """,
    "Card Was Delivered To Me By The Post Office": """On {date}, the Post Office delivered your new card for Receipt Number {receipt_number}, to the address that you gave us.  The tracking number assigned is {tracking_number}.  You can use your tracking number at \t<a href="https://tools.usps.com/go/TrackConfirmAction_input?origTrackNum={tracking_number}" target="_blank">www.USPS.com</a>\t in the Quick Tools Tracking section.  If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t to give us your new mailing address.""",
    "Name Was Updated": """On {date}, we updated your name for your {form_long_name}, Receipt Number {receipt_number}. If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t to give us your new mailing address.""",
    "Request for Additional Evidence Was Sent": """On {date}, we sent a request for additional evidence for your {form_long_name}, Receipt Number {receipt_number}.  The request for evidence explains what we need from you.  We will not take action on your case until we receive the evidence or the deadline to submit it expires. Please follow the instructions in the request for evidence.  If you do not receive your request for additional evidence by {notice_deadline}, please go to \t<a href="https://egov.uscis.gov/e-Request/Intro.do" target="_blank">www.uscis.gov/e-request</a>\t  to request a copy.  If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t  to give us your new mailing address.""",
    "Notice Explaining USCIS Actions Was Mailed": """On {date}, we began reviewing your {form_long_name}, Receipt Number {receipt_number}.  We mailed you a notice informing you of the action we intend to take on your case.  Please follow the instructions in the notice and submit any requested materials.  If you do not receive your notice by {notice_deadline}, contact the USCIS Contact Center at \t<a href="https://www.uscis.gov/contactcenter" target="_blank">www.uscis.gov/contactcenter</a>\t.  If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t  to give us your new mailing address. """,
}

sep_key_value = ":"
sep_entries = "|"


def match(s, template):
    return re.match(pattern=template.replace("{", "(?P<").replace("}", ">.*)"), string=s).groupdict()


def get_arguments_from_string(s, status):
    try:
        template = status_to_msg[status]
    except KeyError as e:
        print("Missing Status", status, e)
        template = "{content}"
        status_to_msg[status] = template
    return match(s=s, template=template)


def rebuild_string_from_template(status, **kwargs):
    template = status_to_msg[status]
    return template.format(**kwargs)


def args_to_string(d):
    return sep_entries.join([sep_key_value.join([k, v]) for k, v in d.items()])


def string_to_args(s):
    return dict(tuple(u.split(sep_key_value, 1)) for u in s.split(sep_entries))


if __name__ == "__main__":

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
