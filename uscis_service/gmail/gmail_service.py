import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
SCOPES = ['https://mail.google.com/']


"""Shows basic usage of the Gmail API.
Lists the user's Gmail labels.
"""
creds = None
token_name = 'token.pickle'
credential_file = 'credentials.json'
user_id = 'me'
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists(token_name):
    with open(token_name, 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            credential_file, SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open(token_name, 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)
