import re


status_to_msg = {
    " Premium Processing Fee Will Be Refunded":
        "On {date}, USCIS made the decision to refund the Premium Processing fee for your {form_long_name}, "
        "Receipt Number {receipt_number}. "
        "Your refund will be mailed to the fee remitter on file. "
        "This refund does not affect the processing or location of your case. "
        "If you do not receive your refund by {notice_deadline}, "
        "please call the Burlington Finance Center at 1-802-288-7600. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Advance Parole Document Was Produced":
        "On {date}, we produced your Advance Parole Document for your {form_long_name}, "
        "Receipt Number {receipt_number}. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Amended Notice Was Mailed":
        "On {date}, we sent you an amended notice describing how we will process your {form_long_name}, "
        "Receipt Number {receipt_number}.¿ It is being processed at our National Benefits Center location. "
        "Please follow any instructions in the notice. "
        "If you do not receive your amended notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Appeal Was Approved":
        "The appellate authority approved your appeal and mailed you a decision. "
        "Your case, Receipt Number {receipt_number}, "
        "is being transferred back to the originating office for completion. "
        "If you do not hear from the originating office by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Appeal Was Dismissed":
        "Your appeal was dismissed and the original decision on your case, "
        "Receipt Number {receipt_number}, remains the same. "
        "On {date}, we sent you a notice about this action. "
        "If you do not receive your notice by {notice_deadline}, please contact the appellate authority directly. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Appeal Was Terminated and A Notice Was Mailed To Me":
        "We terminated your appeal for {form_long_name}, Receipt Number {receipt_number}, "
        "and mailed you a termination notice. "
        "Please follow the instructions in the notice. "
        "If you do not receive your notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Biometrics Appointment Was Scheduled":
        "On {date}, we scheduled you for a biometrics appointment and sent you an appointment notice "
        "for Receipt Number {receipt_number}. "
        "Please follow the instructions in the notice. "
        "If you do not receive your appointment notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Card Destroyed":
        "On {date}, we destroyed your card for Receipt Number {receipt_number}, "
        "that you returned to us with a letter of explanation. "
        "We will inform you if any further action or information is necessary. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Card Is Being Returned to USCIS by Post Office":
        "On {date}, the Post Office reported that they are returning your new card "
        "for Receipt Number {receipt_number}, to us. "
        "We mailed your card to the address you gave us, but the Post Office could not deliver it. "
        "The tracking number assigned is {tracking_number}. "
        "You can use your tracking number at www.USPS.com in the Quick Tools Tracking section. "
        "Please go to www.uscis.gov/e-request to request that we resend the card to you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Card Was Delivered To Me By The Post Office":
        "On {date}, the Post Office delivered your new card for Receipt Number {receipt_number}, "
        "to the address that you gave us. The tracking number assigned is {tracking_number}. "
        "You can use your tracking number at www.USPS.com in the Quick Tools Tracking section. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Card Was Destroyed":
        "On {date}, we destroyed your card for your {form_long_name}, Receipt Number {receipt_number}, "
        "because the Post Office returned it and we did not hear from you. "
        "You must file a {form_long_name_2}, with the correct fee to obtain a new card. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Card Was Mailed To Me":
        "On {date}, we mailed your new card for your {form_long_name}, Receipt Number {receipt_number}, "
        "to the address you gave us. If you do not receive your card by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request that we {send_phrase}. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Card Was Picked Up By The United States Postal Service":
        "On {date}, the Post Office picked up mail containing your new card for Receipt Number {receipt_number}. "
        "We mailed your card to the address you gave us. The tracking number assigned is {tracking_number}. "
        "You can use your tracking number at www.USPS.com in the Quick Tools Tracking section. "
        "If you did not receive the card, please go to www.uscis.gov/e-request "
        "to request that we resend the card to you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Rejected Because My Check Or Money Order Is Not Signed":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because your check or money order was not signed. "
        "We mailed your case back to you, including supporting materials and the unsigned check or money order. "
        "Please follow the instructions to resubmit your case. "
        "If you do not receive your rejected case by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Reopened":
        "On {date}, we {phrasing_1} {form_long_name}, Receipt Number {receipt_number}, {phrasing_2}. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Card Was Returned To USCIS":
        "On {date}, the Post Office returned your new card for {form_long_name}, "
        "Receipt Number {receipt_number}, to us. "
        "We mailed your card to the address you gave us, but the Post Office could not deliver it."
        "{more_inconsistent_tabs} assigned is {tracking_number}. "
        "You can use your tracking number at www.USPS.com in the {section_path} section. "
        "We will destroy your new card if we do not receive an address update by {notice_deadline}. "
        "Please go to{inconsistent_tabs}to request that we resend the card to you. If you move, {truncated_message}",
    "Case Accepted By The USCIS Lockbox":
        "On {date}, we accepted your {form_long_name}, Receipt Number {receipt_number}, "
        "and mailed you a notice describing how we will process your case. "
        "Please follow the instructions in the notice. "
        "If you do not receive your receipt notice by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Approval Was Certified By USCIS":
        "On {date}, we certified the approval of your {form_long_name}, Receipt Number {receipt_number}, "
        "and sent it to the appropriate appellate office. "
        "That office will send you a final decision. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Approval Was Reaffirmed And Mailed Back To Department Of State":
        "On {date}, the Department of State returned your case, Receipt Number {receipt_number}, "
        "to us for further review and we mailed you a notice affirming our original approval. "
        "Please contact the Department of State directly for any further information on your case.",
    "Case Closed Benefit Received By Other Means":
        "On {date}, we closed your {form_long_name}, Receipt Number {receipt_number}, "
        "because the applicant or petitioner received a status or benefit through other means. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Is On Hold Because Of Pending Litigation":
        "On {date}, we placed your {form_long_name}, Receipt Number {receipt_number}, "
        "on hold because there is pending litigation that may affect the outcome. "
        "We will start working on your case as soon as the litigation is resolved. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case is Ready to Be Scheduled for An Interview":
        "As of {date}, we are ready to schedule your {form_long_name}, "
        "Receipt Number {receipt_number}, for an interview. We will schedule your interview and send you a notice. "
        "Please follow any instructions in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Rejected Because I Sent An Incorrect Fee":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because you sent us the incorrect fee. "
        "We mailed your case back to you, including any supporting materials and the incorrect payment. "
        "Please follow the instructions to resubmit your case. "
        "If you do not receive your rejected case by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Rejected Because The Version Of The Form I Sent Is No Longer Accepted":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because you used an old version of the form that we no longer accept. "
        "We mailed your case back to you, including any supporting materials and the payment. "
        "Please follow the instructions to resubmit your case. "
        "If you do not receive your rejected case by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Rejected For Form Not Signed And Incorrect Form Version":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because you did not sign the form and we no longer accept the version of the form you used. "
        "We mailed your case back to you, including any supporting materials and the payment. "
        "Please follow the instructions to resubmit your case. "
        "If you do not receive your rejected case by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Rejected For Incorrect Fee And Form Not Signed":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because you did not sign the form and the fee you paid was incorrect. "
        "We mailed your case back to you, including any supporting materials and the payment. "
        "Please follow the instructions to resubmit your case. "
        "If you do not receive your rejected case by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Rejected For Incorrect Fee And Incorrect Form Version":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because the fee you paid was incorrect and we no longer accept the version of the form you used. "
        "We mailed your case back to you, including any supporting materials and the incorrect fee. "
        "Please follow the instructions to resubmit your case. "
        "If you do not receive your rejected case by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Rejected For Incorrect Fee And Payment Not Signed":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because your check or money order was not signed and the fee was incorrect. "
        "We mailed your case back to you, including any supporting materials and the incorrect payment. "
        "Please follow the instructions to resubmit your case. "
        "If you do not receive your rejected case by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Rejected For Incorrect Fee, Payment Not Signed And Incorrect Form Version":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because your check or money order was not signed, the fee you paid was incorrect, "
        "and we no longer accept the version of the form you used. "
        "We mailed your case back to you, including any supporting materials, "
        "the unsigned check or money order, and incorrect fee. "
        "Please follow the instructions to resubmit your case. "
        "If you do not receive your rejected case by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "CASE STATUS":
        "At this time USCIS cannot provide you with information for your case. "
        "Please contact the USCIS Contact Center at {phone_number} for additional information.",
    "Case Transferred And New Office Has Jurisdiction":
        "On {date}, your {form_long_name}, Receipt Number {receipt_number}, was transferred to another USCIS office. "
        "That office now has jurisdiction over your case. We sent you a notice that explains why we moved your case. "
        "Please follow the instructions in the notice. "
        "If you do not receive your notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Transferred To Another Office":
        "On {date}, we transferred your {form_long_name}, Receipt Number {receipt_number}, "
        "to another office for processing and sent you a transfer notice. "
        "The notice explains why we transferred your case. Please follow the instructions in the notice. "
        "If you do not receive your notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Approved":
        "On {date}, we approved your {form_long_name}, Receipt Number {receipt_number}. "
        "We sent you an approval notice. Please follow the instructions in the notice. "
        "If you do not receive your approval notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Approved And A Decision Notice Was Sent":
        "We approved your {form_long_name}, Receipt Number {receipt_number}, "
        "and mailed your approval decision to the address you gave us. "
        "Please follow the instructions in the notice. "
        "If you do not receive your approval notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Approved And My Decision Was Emailed":
        "We approved your {form_long_name}, Receipt Number {receipt_number}, and emailed you an approval notice. "
        "Please follow any instructions on the approval notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Automatically Revoked":
        "On {date}, we automatically revoked your {form_long_name}, Receipt Number {receipt_number}. "
        "We will mail you a revocation notice explaining the specific reason(s) for our decision. "
        "Please follow any instructions in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Denied":
        "On {date}, we denied your {form_long_name}, Receipt Number {receipt_number}. "
        "We sent you a denial notice that explains why we denied your case and your options. "
        "Please follow the instructions in the notice. "
        "If you do not receive your denial notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Denied And My Decision Notice Mailed":
        "On {date}, we denied your {form_long_name}, Receipt Number {receipt_number}. "
        "We sent you a decision notice that explains why we denied your case and your options. "
        "Please follow the instructions in the notice. "
        "If you do not receive your denial notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Received":
        "On {date}, we received your {form_long_name}, Receipt Number {receipt_number}, "
        "and sent you the receipt notice that describes how we will process your case. "
        "Please follow the instructions in the notice. "
        "If you do not receive your receipt notice by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Received and A Receipt Notice Was Emailed":
        "On {date}, we received your {form_long_name}, Receipt Number {receipt_number}, "
        "and mailed you a receipt notice or acceptance notice. "
        "It is being processed at our {location_name} location. "
        "The notice describes how we will process your case. "
        "Please follow the instructions in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Received At Another USCIS Office":
        "On {date}, we received your {form_long_name}, Receipt Number {receipt_number}, "
        "at this office for processing from another office. "
        "We mailed you a notice that describes how we will process your case. "
        "Please follow the instructions in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Card Was Received By USCIS Along With My Letter":
        "On {date}, we received your card for Receipt Number {receipt_number}, with a letter from you. "
        "We are reviewing your submission, and will mail you a notice, if necessary. "
        "Please follow any instructions provided in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Rejected Because I Did Not Sign My Form":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because you did not sign your form. We mailed your case back to you, including any supporting materials. "
        "Please follow the instructions to resubmit your case. "
        "If you do not receive your rejected case by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Rejected Because It Was Improperly Filed":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because it was not filed correctly. "
        "We mailed your case back to you, including any supporting materials and fee. "
        "Please follow the instructions to resubmit your case. "
        "If you do not receive your rejected case by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Relocated From Administrative Appeals Office To USCIS Originating Office":
        "On {date}, the Administrative Appeals Office (AAO) transferred your {form_long_name}, "
        "Receipt Number {receipt_number}, to the USCIS office that made the original decision on your case. "
        "That office will mail you our decision or send you a request if it needs something from you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Reopened For Reconsideration":
        "On {date}, we reopened your {form_long_name}, Receipt Number {receipt_number}, "
        "and are reconsidering our earlier decision. "
        "We sent you a notice that describes how we will process your case. "
        "Please follow the instructions in the notice. "
        "If you do not receive your notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Sent To The Administrative Appeals Office for Review":
        "On {date}, we sent your {form_long_name}, Receipt Number {receipt_number}, "
        "to the Administrative Appeals Office (AAO) for review. "
        "That office will mail you our decision or send you a request if it needs something from you. "
        "Please follow any instructions provided to you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Sent To The Department of State":
        "On {date}, we sent your case, Receipt Number {receipt_number}, "
        "to the Department of State for visa processing. "
        "You can find general information on Consular Processing by visiting our website at www.uscis.gov . "
        "The website will provide information on what to do next, who to contact, "
        "and how to inform us of any changes in your situation or address.",
    "Case Was Sent To The Executive Office of Immigration Review":
        "On {date}, we sent your {form_long_name}, Receipt Number {receipt_number}, "
        "to the Executive Office of Immigration Review (EOIR). "
        "That office will mail you our decision or send you a request if it needs something from you. "
        "Please follow any instructions provided to you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Transferred And A New Office Has Jurisdiction":
        "On {date}, we transferred your {form_long_name}, Receipt Number {receipt_number}, to another USCIS office. "
        "That office now has jurisdiction over your case. We sent you a notice that explains why we moved your case. "
        "Please follow the instructions in the notice. "
        "If you do not receive your notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Transferred To An Asylum Office":
        "On {date}, we transferred your {form_long_name}, Receipt Number {receipt_number}, "
        "to an asylum office for processing. "
        "That office will mail you a decision or send you a request if it needs something from you. "
        "Please follow any instructions in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Transferred To International Office/Consulate":
        "On {date}, we transferred your {form_long_name}, Receipt Number {receipt_number}, "
        "as part of standard processing. "
        "Form I-730 Asylee Petitions are transferred to USCIS International Office "
        "or DOS Consulate Office in the country of your beneficiary.s physical residence. "
        "That USCIS office or the National Visa Center will provide you with instructions "
        "regarding the beneficiary.s interview. If the beneficiary relocates to a different country, "
        "contact the USCIS International Office or the DOS Consulate Office in the new country "
        "to request to transfer {form_long_name2}. "
        "Form I-730 Refugee Petitions are transferred to USCIS International Adjudications Support Branch "
        "for further processing. "
        "That USCIS Office will provide you with further instructions upon receipt of your case. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Transferred To Schedule An Interview":
        "On {date}, we transferred your {form_long_name}, Receipt Number {receipt_number}, "
        "to our local USCIS office to have an interview scheduled. "
        "This office will schedule your interview and mail you an interview notice. "
        "If you move before you receive the interview notice, "
        "please go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Updated To Show Fingerprints Were Taken":
        "As of {date}, fingerprints relating to your {form_long_name}, Receipt Number {receipt_number}, "
        "have been applied to your case. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Case Was Updated To Show That No One Appeared for In-Person Processing":
        "On {date}, we requested that certain people associated with your {form_long_name}, "
        "Receipt Number {receipt_number}, come to an appointment. "
        "No one came to the appointment, and this will significantly affect your case. "
        "We will mail you a notice if we make a decision or take further action. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Continuation Notice Was Mailed":
        "On {date}, we mailed you a continuation notice regarding your {form_long_name}, "
        "Receipt Number {receipt_number}. Please follow the instructions in the notice. "
        "If you do not receive your continuation notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Correspondence Was Received And USCIS Is Reviewing It":
        "On {date}, we received your correspondence for {form_long_name}, Receipt Number {receipt_number}. "
        "We are reviewing your correspondence, and will send you a notice if we need something from you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "CWR Notice of Intent to Revoke Sent":
        "On {date}, we mailed you a notice explaining our intent to revoke "
        "our earlier approval of the {form_long_name}, Receipt Number {receipt_number}, "
        "based on failure to file your required Semiannual Report for CW-1 Employers (Form I-129CWR). "
        "The notice provides guidance on what you must do in order to avoid revocation of this petition "
        "and denial of your future petitions. "
        "Please follow the instructions in the notice and submit any requested materials. "
        "If you do not receive your notice by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Date of Birth Was Updated":
        "On {date}, we updated your date of birth for your {form_long_name}, Receipt Number {receipt_number}. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Department of State Sent Case to USCIS For Review":
        "On {date}, the Department of State sent us your case, Receipt Number {receipt_number}, for review. "
        "We are reviewing it, and will notify you by mail when we are done. "
        "Please follow any instructions in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Document Destroyed":
        "On {date}, we destroyed your document for your {form_long_name}, Receipt Number {receipt_number}, "
        "because the Post Office returned it and we did not hear from you. "
        "You must file a {form_long_name_2}, with the correct fee to obtain a new document. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Document Was Destroyed And Letter Was Received":
        "On {date}, we destroyed your document for your {form_long_name}, Receipt Number {receipt_number}. "
        "We are reviewing your letter explaining the reasons for the return. "
        "We will mail you a notice, if necessary. "
        "If we send you a notice, please follow any instructions on that notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Document Was Mailed":
        "We mailed your document for your {form_long_name}, Receipt Number {receipt_number}. "
        "If you do not receive your document by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request that we resend the document to you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Document Was Mailed To Me":
        "On {date}, we mailed your document for Receipt Number {receipt_number}, directly to the address you gave us. "
        "If you do not receive your document by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request the document be sent to you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Duplicate Notice Was Mailed":
        "On {date}, we sent you a duplicate notice about a decision on your {form_long_name}, "
        "Receipt Number {receipt_number}, or describing how we will process the case if it is still pending. "
        "Your case is located at our {location_name} location. Please follow any instructions in the notice. "
        "If you do not receive your duplicate notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Eligibility Notice Was Mailed":
        "On {date}, we mailed you a notice informing you that you are eligible for {form_long_name}, "
        "Receipt Number {receipt_number}. Please follow the instructions in the notice. "
        "If you do not receive your notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Expedite Request Approved":
        "On {date}, we approved your request for expedite processing on your {form_long_name}, "
        "Receipt Number {receipt_number}. "
        "We are processing your case and will send you a notice of action with our final decision. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Expedite Request Denied":
        "On {date}, we denied your request for expedite processing of your {form_long_name}, "
        "Receipt Number {receipt_number}. You did not provide evidence of an extreme emergent need. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Expedite Request Received":
        "On {date}, we received your request for expedited processing on your {form_long_name}, "
        "Receipt Number {receipt_number}. "
        "We are reviewing your request and will notify you if we need additional information. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Fee Refund Was Mailed":
        "On {date}, USCIS refunded the fee for your {form_long_name}, Receipt Number {receipt_number}, "
        "and mailed the refund to the address of the fee remitter on file. "
        "This refund does not affect the processing or location of your case. "
        "If the fee remitter does not receive a refund by {notice_deadline}, "
        "please call the Burlington Finance Center at 1-802-288-7600. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Fee Will Be Refunded":
        "On {date}, USCIS made the decision to refund the fee for your {form_long_name}, "
        "Receipt Number {receipt_number}. Your refund will be mailed to the fee remitter on file. "
        "This refund does not affect the processing or location of your case. "
        "If you do not receive your refund by {notice_deadline}, "
        "please call the Burlington Finance Center at 1-802-288-7600. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Fees Were Waived":
        "On {date}, we received your case and waived the filing fee for your {form_long_name}, "
        "Receipt Number {receipt_number}. We mailed you a notice describing how we will process your case. "
        "Please follow the instructions in the notice. "
        "If you do not receive your receipt notice by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Filed Under Known Employer Pilot":
        "On {date}, we received your {form_long_name}, Receipt Number {receipt_number}. "
        "Your case has been filed under the Known Employer pilot. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Fingerprint and Biometrics Appointment Was Scheduled":
        "On {date}, we scheduled you for a fingerprint and biometrics appointment "
        "and mailed you an appointment notice for Receipt Number {receipt_number}. "
        "Please follow the instructions in the notice. "
        "If you do not receive your appointment notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Fingerprint Fee Was Received":
        "On {date}, we accepted the fingerprint fee for your {form_long_name}, Receipt Number {receipt_number}. "
        "Our {location_name} location is working on your case. "
        "We mailed you a notice describing how we will process your case. "
        "Please follow the instructions in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Form G-28 Was Rejected Because It Was Improperly Filed":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number}, "
        "because it was not filed correctly. "
        "If you wish to be represented, "
        "please contact your attorney or accredited representative to submit a new Form G-28 "
        "to the USCIS location where your case is pending. "
        "For more information on filing a Form G-28, "
        "please visit http://www.uscis.gov/forms/filing-your-form-g-28. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Intent to Revoke Notice Was Sent":
        "On {date}, we mailed you a notice explaining our intent to revoke our earlier approval of your case, "
        "Receipt Number {receipt_number}. The notice explains what we will do. "
        "Please follow the instructions in the notice and submit any requested materials. "
        "If you do not receive your notice before {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Interview Cancelled":
        "On {date}, we cancelled or descheduled the interview scheduled for your {form_long_name}, "
        "Receipt Number {receipt_number}. "
        "We will notify you by mail if the appointment is rescheduled, a decision is made, "
        "or if the office needs something from you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Interview Cancelled And Notice Ordered":
        "On {date}, we cancelled your interview for your {form_long_name}, Receipt Number {receipt_number}, "
        "and mailed you a cancellation notice. "
        "We will notify you by mail if the appointment is rescheduled, a decision is made, "
        "or if we need something from you. Please follow any instructions in the notice. "
        "If you do not receive your notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Interview Was Completed And My Case Must Be Reviewed":
        "Your interview for your {form_long_name}, Receipt Number {receipt_number}, was completed, "
        "and your case must be reviewed. We will mail you a notice if we make a decision or take further action. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Interview Was Rescheduled":
        "On {date}, we rescheduled an interview for your {form_long_name}, Receipt Number {receipt_number}. "
        "We will mail you an interview notice. Please follow any instructions in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Interview Was Scheduled":
        "On {date}, we scheduled an interview for your {form_long_name}, Receipt Number {receipt_number}. "
        "We will mail you an interview notice. Please follow any instructions in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Litigation Notice Was Mailed":
        "On {date}, we mailed you a notice informing you about litigation related to your {form_long_name}, "
        "Receipt Number {receipt_number}. Please follow the instructions in the notice. "
        "If you do not receive your notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Name Was Updated":
        "On {date}, we updated your name for your {form_long_name}, Receipt Number {receipt_number}. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "New Card Is Being Produced":
        "On {date}, we ordered your new card for Receipt Number {receipt_number}, "
        "and will mail it to the address you gave us. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Notice Explaining USCIS Actions Was Mailed":
        "On {date}, we began reviewing your {form_long_name}, Receipt Number {receipt_number}. "
        "We mailed you a notice informing you of the action we intend to take on your case. "
        "Please follow the instructions in the notice and submit any requested materials. "
        "If you do not receive your notice by {notice_deadline}, "
        "contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Notice Was Returned To USCIS Because The Post Office Could Not Deliver It":
        "On {date}, the Post Office returned a notice we sent you for your {form_long_name}, "
        "Receipt Number {receipt_number}, because they could not deliver it. "
        "This could have a serious effect on your case. "
        "Please go to www.uscis.gov/e-request to request a copy of the notice immediately. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Petition/Application Was Rejected For Insufficient Funds":
        "On {date}, we rejected your {form_long_name}, Receipt Number {receipt_number} "
        "because your filing fee was returned by your financial institution for insufficient funds. "
        "Any previously assigned priority or processing date is no longer applicable. "
        "If you wish to still pursue the benefit, "
        "you must file a new application or petition and submit a new fee filing fee. "
        "If you need assistance, contact the USCIS Contact Center at www.uscis.gov/contactcenter. "
        "If you change your mailing address, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Premium Processing Case is Eligible for Pre-Certification":
        "On {date}, we determined that the business sponsor for your {form_long_name}, "
        "Receipt Number {receipt_number}, meets our pre-certification requirements. "
        "Your premium-processing receipt notice contains contact information for direct inquiries on your case. "
        "Please follow the instructions in the notice. "
        "If you move, contact the premium-processing unit directly to update your address.",
    "Premium Processing Case is Not Eligible for Pre-Certification":
        "On {date}, we determined that your {form_long_name}, Receipt Number {receipt_number}, "
        "is not eligible for pre-certification. "
        "Additional documentation may be necessary for further processing. "
        "Your premium-processing receipt notice contains contact information for direct inquiries on your case. "
        "Please follow the instructions in the notice. "
        "If you move, contact the premium-processing unit directly to update your address.",
    "Reentry Permit Was Produced":
        "On {date}, we produced your Reentry Permit for your {form_long_name}, Receipt Number {receipt_number}. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Refugee Travel Document Was Produced":
        "On {date}, we produced your Refugee Travel Document for your {form_long_name}, "
        "Receipt Number {receipt_number}. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Request For A Duplicate Card Was Approved":
        "On {date}, we received your request for a duplicate card for your {form_long_name}, "
        "Receipt Number {receipt_number}, and we approved your request. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Request for Additional Evidence Was Sent":
        "On {date}, we sent a request for additional evidence for your {form_long_name}, "
        "Receipt Number {receipt_number}. The request for evidence explains what we need from you. "
        "We will not take action on your case until we receive the evidence or the deadline to submit it expires. "
        "Please follow the instructions in the request for evidence. "
        "If you do not receive your request for additional evidence by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Request for Additional Information Received":
        "On {date}, we received your response to our request for additional information "
        "regarding expedite processing of your {form_long_name}, Receipt Number {receipt_number}. "
        "Your request has been forwarded to an officer for review. "
        "We will notify you if we need something from you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Request for Initial Evidence Was Sent":
        "On {date}, we sent a request for initial evidence for your {form_long_name}, Receipt Number {receipt_number}. "
        "The request for evidence explains what we need from you. "
        "We will not take action on your case until we receive the evidence or the deadline to submit it expires. "
        "Please follow the instructions in the request for evidence. "
        "If you do not receive your request for evidence by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Request For Premium Processing Services Was Received":
        "On {date}, we received your request for premium-processing of your {form_long_name}, "
        "Receipt Number {receipt_number}, and mailed you a receipt notice. "
        "Your premium-processing receipt notice contains contact information for direct inquiries on your case. "
        "Please follow the instructions in the notice. "
        "If you move, contact the premium-processing unit directly to update your address.",
    "Request To Reschedule My Appointment Was Received":
        "On {date}, we received your request to reschedule your appointment for {form_long_name}, "
        "Receipt Number {receipt_number}. Our National Benefits Center office is reviewing your request. "
        "We will inform you if your appointment is rescheduled and send any notices to the address you gave us. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Response To USCIS' Request For Evidence Was Received":
        "On {date}, we received your response to our Request for Evidence for your {form_long_name}, "
        "Receipt Number {receipt_number}. USCIS has begun working on your case again. "
        "We will send you a decision or notify you if we need something from you. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Revocation Notice Was Sent":
        "On {date}, we revoked the approval of your case, Receipt Number {receipt_number}, "
        "and mailed you a revocation notice. It explains the reasons for our action. "
        "Please follow the instructions in the notice and submit any requested materials. "
        "If you do not receive your revocation notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Status Termination Notice Was Mailed":
        "On {date}, we mailed you a notice for Receipt Number {receipt_number}, terminating your status. "
        "The notice explains the reasons for our action. Please follow the instructions in the notice. "
        "If you do not receive your notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Travel Document Was Destroyed":
        "On {date}, we destroyed your travel document for Receipt Number {receipt_number}, "
        "that you returned to us with a letter of explanation. "
        "We will inform you if any further action or information is necessary. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Travel Document Was Destroyed After USCIS Held It For 180 Days":
        "On {date}, we notified you that the Post Office returned your travel document for "
        "Receipt Number {receipt_number}, to us because they could not deliver it. "
        "We gave you 180 days or until {notice_deadline} to contact us. "
        "The 180 days have passed, and you did not contact us. We have destroyed your document. "
        "If you still need the document, you will have to file a {form_long_name_2}, with fee. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Travel Document Was Mailed":
        "On {date}, we mailed your travel document for Receipt Number {receipt_number}, "
        "to the address you gave us. "
        "If you do not receive your travel document by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request that we resend you the travel document. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Travel Document Was Returned to USCIS And Will Be Held For 180 Days":
        "On {date}, your travel document for Receipt Number {receipt_number}, "
        "was returned to us because the Post Office could not deliver it. "
        "We will hold your travel document until {notice_deadline}. "
        "Please go to www.uscis.gov/e-request to request the travel document. "
        "If you do not submit an online request or contact us at 1-800-375-5283 by {notice_deadline2}, "
        "we will destroy your document and you will need to file a new {form_long_name_2}, with fee. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Travel Document Was Received By USCIS Along With My Letter":
        "On {date}, we received your travel document for Receipt Number {receipt_number}, and letter. "
        "We are reviewing your submission, and will mail you a notice, if necessary. "
        "Please follow any instructions in the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Withdrawal Acknowledgement Notice Was Sent":
        "On {date}, we received your request to withdraw your {form_long_name}, Receipt Number {receipt_number}, "
        "and completed our review. We mailed you a Withdrawal Acknowledgment Notice. "
        "If you do not receive your Withdrawal Acknowledgment Notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    "Withdrawal Of My Appeal Was Acknowledged":
        "On {date}, we mailed you a notice acknowledging withdrawal of your appeal "
        "for Receipt Number {receipt_number}. Your withdrawal ends all action on this appeal. "
        "Please follow the instructions in the notice. "
        "If you do not receive your notice by {notice_deadline}, "
        "please go to www.uscis.gov/e-request to request a copy of the notice. "
        "If you move, go to www.uscis.gov/addresschange to give us your new mailing address.",
    None: "",
}

print("Number of Status Templates", len(status_to_msg.keys()))

sep_key_value = ":"
sep_entries = "|"


def remove_tags(s):
    return ' '.join(re.sub(pattern=r'<[^>]+>', repl='', string=s).split())


def check_title_in_status(title):
    return title in status_to_msg


def get_template(status):
    if check_title_in_status(title=status):
        return status_to_msg[status]
    print("Template not found", status)


def match(s, template):
    s = remove_tags(s=s)
    template_for_paren = template.replace("(", r"\(").replace(")", r"\)")
    mod_template = template_for_paren.replace("{", "(?P<").replace("}", ">.*)")
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
