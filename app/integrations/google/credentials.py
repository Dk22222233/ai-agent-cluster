
from datetime import datetime
from uuid import UUID

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from sqlalchemy.orm import Session

from config import settings
from app.repositories.integration_repo import integration_repo
from app.integrations.google.auth import SCOPES


class GoogleCredentialFactory:
    def __init__(self, db: Session):
        self.db = db
        self.repo = integration_repo

    def get_credentials(self, user_id: UUID) -> Credentials:
        conn = self.repo.get_google_connection(
            user_id=user_id,
            db=self.db,
        )

        if not conn or not conn.refresh_token:
            raise ValueError("Google account is not connected.")

        credentials = Credentials(
            token=conn.access_token,
            refresh_token=conn.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=SCOPES,
            expiry=conn.expires_at,
        )

        if not credentials.valid:
            credentials.refresh(Request())

            self.repo.update_google_tokens(
                user_id=user_id,
                access_token=credentials.token,
                expires_at=credentials.expiry,
                db=self.db,
            )

        return credentials