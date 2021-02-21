import pickle
import os.path
import email
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from lxml import html

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authorize():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_link():
    service = authorize()
    messages = service.users().messages().list(userId='me').execute()
    msg_id = messages['messages'][0]['id']
    message = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
    msg_str = base64.urlsafe_b64decode(message['raw'].encode("utf-8")).decode("utf-8")
    msg = email.message_from_string(msg_str)
    body = ""
    if msg.is_multipart():
        for payload in msg.get_payload():
            body = payload.get_payload(decode=True)
    else:
        body = msg.get_payload()
    body = html.fromstring(body)
    link = body.xpath('//a//@href')[0]
    return link


if __name__ == '__main__':
    authorize()
