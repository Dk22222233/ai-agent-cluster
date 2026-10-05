from fastapi import APIRouter, Depends
from supabase_auth import UserResponse
from api.dependencies import get_current_user


router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me",response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user