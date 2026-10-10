from fastapi import APIRouter, Depends, Query, HTTPException
from api.schemas.user_schema import UserResponse
from app.services.integration_service import integration_service
from api.dependencies import get_current_user
router = APIRouter(prefix='integrator',tags=['Integrations'])
@router.get('/google/connect')
def google_connect(current_user:UserResponse=Depends(get_current_user)):
    user_id=current_user.id
    auth_url=integration_service.start_google_oauth(user_id)
    return {'url':auth_url}

@router.get('/google/callback')
def google_callback(code:str=Query(),state:str=Query(),error:str=Query(default=None)):
    if error:
        raise HTTPException(
            status_code=400,
            detail=f'Google Authorization failed:{error}'
        )
    return integration_service.finish_google_oauth(
        code=code,
        state=state
    )