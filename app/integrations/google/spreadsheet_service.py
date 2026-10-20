from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.integration_repo import integration_repo
from app.integrations.google.credentials import google_credentials_factory
from app.integrations.google.client import get_sheet_client


class SpreadsheetService:
    def __init__(self, db: Session, user_id: UUID):
        self.db = db
        self.user_id = user_id
        self.repo = integration_repo

    def get_client(self):
        conn = self.repo.get_google_connection(
            self.user_id,
            self.db,
        )

        if not conn or not conn.refresh_token:
            raise HTTPException(
                status_code=400,
                detail="Google account not connected. Please connect first.",
            )

        credentials = google_credentials_factory.create(
            access_token=conn.access_token,
            refresh_token=conn.refresh_token,
            expire_at=conn.expires_at,
        )

        if (
            credentials.token != conn.access_token
            or credentials.expiry != conn.expires_at
        ):
            self.repo.update_google_tokens(
                user_id=self.user_id,
                access_token=credentials.token,
                expires_at=credentials.expiry,
                db=self.db,
            )

        return get_sheet_client(credentials)