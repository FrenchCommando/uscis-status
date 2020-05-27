import re


status_to_msg = {
    "Card Is Being Returned to USCIS by Post Office": """On {date}, the Post Office reported that they are returning your new card for Receipt Number {receipt_number}, to us. We mailed your card to the address you gave us, but the Post Office could not deliver it. The tracking number assigned is {tracking_number}. You can use your tracking number at \twww.USPS.com\t in the Quick Tools Tracking section. Please go to \twww.uscis.gov/e-request\t to request that we resend the card to you. If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Card Was Delivered To Me By The Post Office": """On {date}, the Post Office delivered your new card for Receipt Number {receipt_number}, to the address that you gave us.  The tracking number assigned is {tracking_number}.  You can use your tracking number at \twww.USPS.com\t in the Quick Tools Tracking section.  If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Card Was Mailed To Me": """On {date}, we mailed your new card for your {form_long_name}, Receipt Number {receipt_number}, to the address you gave us.  If you do not receive your card by {notice_deadline}, please go to \twww.uscis.gov/e-request\t  to request that we {send_phrase}.  If you move, go to \twww.uscis.gov/addresschange\t  to give us your new mailing address.""",
    "Card Was Picked Up By The United States Postal Service": """On {date}, the Post Office picked up mail containing your new card for Receipt Number {receipt_number}. We mailed your card to the address you gave us. The tracking number assigned is {tracking_number}. You can use your tracking number at \twww.USPS.com\t in the Quick Tools Tracking section. If you did not receive the card, please go to \twww.uscis.gov/e-request\t to request that we resend the card to you. If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Case Rejected Because I Sent An Incorrect Fee": """On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, because you sent us the incorrect fee.  We mailed your case back to you, including any supporting materials and the incorrect payment.  Please follow the instructions to resubmit your case.  If you do not receive your rejected case by {notice_deadline}, contact the USCIS Contact Center at \twww.uscis.gov/contactcenter\t.  If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Case Rejected Because The Version Of The Form I Sent Is No Longer Accepted": """On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, because you used an old version of the form that we no longer accept.  We mailed your case back to you, including any supporting materials and the payment.  Please follow the instructions to resubmit your case.  If you do not receive your rejected case by {notice_deadline}, contact the USCIS Contact Center at \twww.uscis.gov/contactcenter\t.  If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Case Transferred And New Office Has Jurisdiction": """On {date}, your {form_long_name}, Receipt Number {receipt_number}, was transferred to another USCIS office. That office now has jurisdiction over your case. We sent you a notice that explains why we moved your case. Please follow the instructions in the notice. If you do not receive your notice by {notice_deadline}, please go to \twww.uscis.gov/e-request\t to request a copy of the notice. If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Case Was Approved": """On {date}, we approved your {form_long_name}, Receipt Number {receipt_number}.  We sent you an approval notice.  Please follow the instructions in the notice. If you do not receive your approval notice by {notice_deadline}, please go to \twww.uscis.gov/e-request\t.  If you move, go to \twww.uscis.gov/addresschange\t  to give us your new mailing address.  """,
    "Case Was Received": """On {date}, we received your {form_long_name}, Receipt Number {receipt_number}, and sent you the receipt notice that describes how we will process your case.  Please follow the instructions in the notice.  If you do not receive your receipt notice by {notice_deadline}, contact the USCIS Contact Center at \twww.uscis.gov/contactcenter\t.  If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Case Was Rejected Because I Did Not Sign My Form": """On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, because you did not sign your form.  We mailed your case back to you, including any supporting materials.  Please follow the instructions to resubmit your case.  If you do not receive your rejected case by {notice_deadline}, contact the USCIS Contact Center at \twww.uscis.gov/contactcenter\t.  If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address. """,
    "Case Was Rejected Because It Was Improperly Filed": """On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, because it was not filed correctly.  We mailed your case back to you, including any supporting materials and fee.  Please follow the instructions to resubmit your case.  If you do not receive your rejected case by {notice_deadline}, contact the USCIS Contact Center at \twww.uscis.gov/contactcenter\t.  If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address. """,
    "Case Was Sent To The Department of State": """On {date}, we sent your case, Receipt Number {receipt_number}, to the Department of State for visa processing.  You can find general information on Consular Processing by visiting our website at www.uscis.gov .  The website will provide information on what to do next, who to contact, and how to inform us of any changes in your situation or address.""",
    "Case Was Updated To Show Fingerprints Were Taken": """As of {date}, fingerprints relating to your {form_long_name}, Receipt Number {receipt_number}, have been applied to your case.  If you move, go to \twww.uscis.gov/addresschange\t  to give us your new mailing address.""",
    "Date of Birth Was Updated": """On {date}, we updated your date of birth for your {form_long_name}, Receipt Number {receipt_number}. If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Fee Will Be Refunded": """On {date}, USCIS made the decision to refund the fee for your {form_long_name}, Receipt Number {receipt_number}.  Your refund will be mailed to the fee remitter on file. This refund does not affect the processing or location of your case.  If you do not receive your refund by {notice_deadline}, please call the Burlington Finance Center at 1-802-288-7600. If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Fees Were Waived": """On {date}, we received your case and waived the filing fee for your {form_long_name}, Receipt Number {receipt_number}.  We mailed you a notice describing how we will process your case.  Please follow the instructions in the notice.  If you do not receive your receipt notice by {notice_deadline}, contact the USCIS Contact Center at \twww.uscis.gov/contactcenter\t.  If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Fingerprint Fee Was Received": """On {date}, we accepted the fingerprint fee for your {form_long_name}, Receipt Number {receipt_number}. Our Nebraska Service Center location is working on your case. We mailed you a notice describing how we will process your case. Please follow the instructions in the notice. If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Form G-28 Was Rejected Because It Was Improperly Filed": """On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, because it was not filed correctly.  If you wish to be represented, please contact your attorney or accredited representative to submit a new Form G-28 to the USCIS location where your case is pending. For more information on filing a Form G-28, please visit \t http://www.uscis.gov/forms/filing-your-form-g-28\t.  If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Name Was Updated": """On {date}, we updated your name for your {form_long_name}, Receipt Number {receipt_number}. If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "New Card Is Being Produced": """On {date}, we ordered your new card for Receipt Number {receipt_number}, and will mail it to the address you gave us. If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Notice Explaining USCIS Actions Was Mailed": """On {date}, we began reviewing your {form_long_name}, Receipt Number {receipt_number}.  We mailed you a notice informing you of the action we intend to take on your case.  Please follow the instructions in the notice and submit any requested materials.  If you do not receive your notice by {notice_deadline}, contact the USCIS Contact Center at \twww.uscis.gov/contactcenter\t.  If you move, go to \twww.uscis.gov/addresschange\t  to give us your new mailing address. """,
    "Notice Was Returned To USCIS Because The Post Office Could Not Deliver It": """On {date}, the Post Office returned a notice we sent you for your {form_long_name}, Receipt Number {receipt_number}, because they could not deliver it. This could have a serious effect on your case. Please go to \twww.uscis.gov/e-request\t to request a copy of the notice immediately. If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    "Request for Additional Evidence Was Sent": """On {date}, we sent a request for additional evidence for your {form_long_name}, Receipt Number {receipt_number}.  The request for evidence explains what we need from you.  We will not take action on your case until we receive the evidence or the deadline to submit it expires. Please follow the instructions in the request for evidence.  If you do not receive your request for additional evidence by {notice_deadline}, please go to \twww.uscis.gov/e-request\t  to request a copy.  If you move, go to \twww.uscis.gov/addresschange\t  to give us your new mailing address.""",
    "Response To USCIS' Request For Evidence Was Received": """On {date}, we received your response to our Request for Evidence for your Form {form_long_name}, Receipt Number {receipt_number}.  USCIS has begun working on your case again.  We will send you a decision or notify you if we need something from you.  If you move, go to \twww.uscis.gov/addresschange\t  to give us your new mailing address.""",
    "Withdrawal Acknowledgement Notice Was Sent": """On {date}, we received your request to withdraw your {form_long_name}, Receipt Number {receipt_number}, and completed our review. We mailed you a Withdrawal Acknowledgment Notice. If you do not receive your Withdrawal Acknowledgment Notice by {notice_deadline}, please go to \twww.uscis.gov/e-request\t to request a copy of the notice. If you move, go to \twww.uscis.gov/addresschange\t to give us your new mailing address.""",
    None: "",
}

sep_key_value = ":"
sep_entries = "|"


def remove_tags(s):
    return re.sub(pattern=r'<[^>]+>', repl='', string=s)


def check_title_in_status(title):
    return title in status_to_msg


def get_template(status):
    return status_to_msg[status]


def match(s, template):
    s = remove_tags(s=s)
    mod_template = template.replace("{", "(?P<").replace("}", ">.*)")
    # print(mod_template)
    # print(s)
    return re.match(pattern=mod_template, string=s).groupdict()


def get_arguments_from_string(s, status):
    try:
        template = status_to_msg[status]
    except KeyError as e:
        print("Missing Status", status, e)
        return
    return match(s=s, template=template)


def rebuild_string_from_template(status, **kwargs):
    template = status_to_msg[status]
    return template.format(**kwargs)


def args_to_string(d):
    return sep_entries.join([sep_key_value.join([k, v]) for k, v in d.items()])


def string_to_args(s):
    return dict(tuple(u.split(sep_key_value, 1)) for u in s.split(sep_entries))
