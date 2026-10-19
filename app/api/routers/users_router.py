from fastapi import APIRouter, Depends
from app.api.schemas.user_schema import UserResponse
from app.api.dependencies import get_current_user,get_db
from app.services import user_service
from sqlalchemy.orm import Session
router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me",response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user),db:Session=Depends(get_db)):
    return user_service.create_user(user=current_user,db=db)