status_to_msg = {
    "Case Was Received": """On {date}, we received your {form_long_name}, Receipt Number {receipt_number}, and sent you the receipt notice that describes how we will process your case.  Please follow the instructions in the notice.  If you do not receive your receipt notice by {notice_deadline}, contact the USCIS Contact Center at \t<a href="https://www.uscis.gov/contactcenter" target="_blank">www.uscis.gov/contactcenter</a>\t.  If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t to give us your new mailing address.""",
    "Case Was Approved": """On {date}, we approved your {form_long_name}, Receipt Number {receipt_number}.  We sent you an approval notice.  Please follow the instructions in the notice. If you do not receive your approval notice by {notice_deadline}, please go to \t<a href="https://egov.uscis.gov/e-Request/Intro.do" target="_blank">www.uscis.gov/e-request</a>\t.  If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t  to give us your new mailing address.  """,
    "Card Was Delivered To Me By The Post Office": """On {date}, the Post Office delivered your new card for Receipt Number {receipt_number}, to the address that you gave us.  The tracking number assigned is {tracking_number}.  You can use your tracking number at \t<a href="https://tools.usps.com/go/TrackConfirmAction_input?origTrackNum=9205590153708669965045" target="_blank">www.USPS.com</a>\t in the Quick Tools Tracking section.  If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t to give us your new mailing address.""",
    "Name Was Updated": """On {date}, we updated your name for your {form_long_name}, Receipt Number {receipt_number}. If you move, go to \t<a href="https://egov.uscis.gov/coa/displayCOAForm.do" target="_blank">www.uscis.gov/addresschange</a>\t to give us your new mailing address.""",
}


if __name__ == "__main__":

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
