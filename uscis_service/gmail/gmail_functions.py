import base64
from email.mime.text import MIMEText
from gmail.gmail_service import load_creds, user_id


def send(subject, body):
    try:
        print("Loading creds")
        service = load_creds()
        message = MIMEText(body)
        message['to'] = "martialren@gmail.com"
        message['subject'] = subject
        message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        service.users().messages().send(userId=user_id, body=message).execute()
    except BaseException as e:
        print(f"Something went wrong in the email stuff - I won't kill myself about it:\t{e}")
