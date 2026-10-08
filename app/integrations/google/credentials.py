import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES=[
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]
BASE_DIR=os.path.dirname(
    os.path.abspath(__name__)
)
TOKEN_PATH=os.path.join(
BASE_DIR,
'token.json'
)
CRED_PATH=os.path.join(
    BASE_DIR,
    'credentials.json'
)
def get_credentails():
    cred=None
    if os.path.exists(TOKEN_PATH):
        cred=Credentials.from_authorized_user_file(TOKEN_PATH,SCOPES)
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())

        else:
            flow=InstalledAppFlow.from_client_secrets_file(
                CRED_PATH,
                SCOPES
            )
            cred=flow.run_local_server(
                port=0
            )
            return cred
