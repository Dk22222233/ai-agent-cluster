from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database.connection import session
from auth.service import auth_service
security = HTTPBearer()
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    access_token = credentials.credentials
    try:
        user=auth_service.get_user(access_token)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_db():
    db:Session=session()
    try:
        yield db
    finally:
        db.close()