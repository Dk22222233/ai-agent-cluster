from datetime import datetime
from uuid import UUID

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from sqlalchemy.orm import Session

from config import settings
from app.repositories.integration_repo import integration_repo
from app.integrations.google.auth import SCOPES

# Import your project's logger
from agent import get_logger

logger = get_logger(__name__)

class GoogleCredentialFactory:
    def __init__(self, db):
        # Log exactly what the factory receives
        logger.debug(f"Initializing GoogleCredentialFactory with db={db} (type={type(db)})")
        self.db = db
        self.repo = integration_repo

    def get_credentials(self, user_id: UUID) -> Credentials:
        logger.debug(f"get_credentials called for user_id={user_id}, using self.db={self.db}")
        
        conn = self.repo.get_google_connection(
            user_id=user_id,
            db=self.db,
        )

        if not conn or not conn.refresh_token:
            logger.warning(f"No Google connection or refresh_token found for user {user_id}")
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
            logger.info(f"Refreshing expired Google token for user {user_id}")
            credentials.refresh(Request())

            self.repo.update_google_tokens(
                user_id=user_id,
                access_token=credentials.token,
                expires_at=credentials.expiry,
                db=self.db,
            )
            logger.info(f"Token refreshed and saved for user {user_id}")

        return credentials