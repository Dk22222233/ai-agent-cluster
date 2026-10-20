from google.oauth2.credentials import Credentials
from datetime import datetime, timezone
from google.auth.transport.requests import Request
from config import settings
from app.integrations.google.auth import SCOPES
class GoogleCredentialFactory:
    def create(
            self,
            access_token:str|None,
            refresh_token:str,
            expire_at:datetime|None=None
        )->Credentials:
        
        credentials=Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=SCOPES,
            expiry=expire_at
        )
        if not credentials.valid:
            credentials.refresh(Request())
        return credentials

google_credentials_factory=GoogleCredentialFactory()
