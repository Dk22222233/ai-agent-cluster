from fastapi import APIRouter, Depends
from api.schemas.user_schema import UserResponse
from api.dependencies import get_current_user
router = APIRouter(prefix='integrator',tags=['Integrations'])
@router.get('/google/connect')
def google_connect(current_user:UserResponse=Depends(get_current_user)):
    pass