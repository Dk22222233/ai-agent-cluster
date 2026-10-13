from sqlalchemy import select
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from config import settings
from uuid import UUID
from app.models.integration_model import IntegrationModel
ENCRYPTION_KEY=settings.OAUTH_TOKEN_ENCRYPTION_KEY
cipher=Fernet(ENCRYPTION_KEY.encode())
class IntegrationRepo:
    def get_google_connection(self,user_id:UUID,db:Session):
        stmt=select(IntegrationModel).where(
            IntegrationModel.user_id==user_id
        )
        # on multplie rows access will later cause errors and for safety we have to keep multiple constrains
        connection=db.execute(stmt).scalar_one_or_none()
        if connection and connection.refresh_token:
            connection.refresh_token=cipher.decrypt(connection.refresh_token.encode()).decode()
        return connection

    def save_google_connection(self,user_id:UUID,refresh_token,db:Session):
        encrypted_refresh=cipher.encrypt(refresh_token.encode()).decode()
        connection=IntegrationModel(
            user_id=user_id,
            refresh_token=encrypted_refresh,
            provider='Google' # HardCoded Provider
        )
        db.add(connection)
        db.commit()
        db.refresh(connection)
        return connection
integration_repo=IntegrationRepo()