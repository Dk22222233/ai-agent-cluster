from datetime import datetime, timezone
from uuid import UUID

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from sqlalchemy.orm import Session

from config import settings
from app.repositories.integration_repo import integration_repo

# Import your project's logger
from agent import get_logger

logger = get_logger(__name__)

class GoogleCredentialFactory:
    def __init__(self, db, integration_key: str | None = None):
        # Log exactly what the factory receives
        logger.debug(f"Initializing GoogleCredentialFactory with db={db} (type={type(db)})")
        self.db = db
        # App-specific providers pass their key so disabled or uninstalled apps cannot invoke tools.
        self.integration_key = integration_key
        self.repo = integration_repo

    @staticmethod
    def _as_utc(value: datetime | None) -> datetime | None:
        # PostgreSQL/driver combinations can return TIMESTAMPTZ as a naive datetime.
        # Google credentials compare expiry against aware UTC timestamps, so normalize at this boundary.
        if value is not None and value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    def get_credentials(self, user_id: UUID) -> Credentials:
        logger.debug(f"get_credentials called for user_id={user_id}, using self.db={self.db}")
        
        conn = self.repo.get_google_connection(
            user_id=user_id,
            db=self.db,
        )

        if not conn or not conn.refresh_token:
            logger.warning(f"No Google connection or refresh_token found for user {user_id}")
            raise ValueError("Google account is not connected.")

        # A shared Google token alone is insufficient; the requested app installation must be enabled.
        if self.integration_key:
            from app.repositories.integration_installation_repo import integration_installation_repo

            installation = integration_installation_repo.get_for_user(
                user_id=user_id,
                integration_key=self.integration_key,
                db=self.db,
            )
            if installation is None or not installation[1].enabled or installation[1].status != "connected":
                raise ValueError(f"{self.integration_key} is not connected or enabled.")

        credentials = Credentials(
            token=conn.access_token,
            refresh_token=conn.refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            # Preserve Google's granted scopes across refreshes on the shared account token.
            scopes=None,
            expiry=self._as_utc(conn.expires_at),
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
