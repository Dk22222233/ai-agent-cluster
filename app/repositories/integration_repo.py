from sqlalchemy.orm import Session
from uuid import UUID
class IntegrationRepo:
    def get_google_connection(user_id:UUID,db:Session):
        pass

    def save_google_connection(user_id:UUID,refresh_token,db:Session):
        pass
integration_repo=IntegrationRepo()