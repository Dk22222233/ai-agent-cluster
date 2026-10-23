from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from config import settings
from uuid import UUID
from agent import get_logger
from app.models.integration_model import IntegrationModel

ENCRYPTION_KEY = settings.OAUTH_TOKEN_ENCRYPTION_KEY
logger = get_logger(__name__)
cipher = Fernet(ENCRYPTION_KEY.encode())

class IntegrationRepo:
    def get_google_connection(self, user_id: UUID, db: Session):
        logger.debug(f"get_google_connection called with user_id={user_id}, db={db} (type={type(db)})")
        stmt = select(IntegrationModel).where(
            IntegrationModel.user_id == user_id,
            IntegrationModel.provider == 'Google'
        )
        connection = db.execute(stmt).scalar_one_or_none()
        
        if connection and connection.refresh_token:
            connection.refresh_token = cipher.decrypt(connection.refresh_token.encode()).decode()
            if connection.access_token:
                connection.access_token = cipher.decrypt(connection.access_token.encode()).decode()
        return connection

    def save_google_connection(self, user_id: UUID, refresh_token: str, access_token: str | None, db: Session):
        # 1. Check if the connection already exists
        stmt = select(IntegrationModel).where(
            IntegrationModel.user_id == user_id,
            IntegrationModel.provider == 'Google'
        )
        existing = db.execute(stmt).scalar_one_or_none()

        encrypted_refresh = cipher.encrypt(refresh_token.encode()).decode()
        encrypted_access = cipher.encrypt(access_token.encode()).decode() if access_token else None

        if existing:
            # 2. Update the existing row
            existing.refresh_token = encrypted_refresh
            if encrypted_access:
                existing.access_token = encrypted_access
        else:
            # 3. Create a new row
            connection = IntegrationModel(
                user_id=user_id,
                refresh_token=encrypted_refresh,
                access_token=encrypted_access,
                provider='Google'
            )
            db.add(connection)

        db.commit()
        
        # Return the row (either updated or newly created)
        return db.execute(stmt).scalar_one()

    def update_google_tokens(self, user_id: UUID, access_token: str, expires_at: datetime, db: Session):
        stmt = select(IntegrationModel).where(
            IntegrationModel.user_id == user_id,
            IntegrationModel.provider == 'Google'
        )
        connection = db.execute(stmt).scalar_one_or_none()
        
        if connection:
            encrypted_access = cipher.encrypt(access_token.encode()).decode()
            connection.access_token = encrypted_access
            connection.expires_at = expires_at
            db.commit()
            db.refresh(connection)
            
        return connection

integration_repo = IntegrationRepo()