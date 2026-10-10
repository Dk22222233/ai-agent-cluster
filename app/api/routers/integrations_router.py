from fastapi import APIRouter, Depends, Query, HTTPException
from api.schemas.user_schema import UserResponse
from sqlalchemy.orm import Session
from app.services.integration_service import integration_service
from api.dependencies import get_current_user, get_db
router = APIRouter(prefix='integrator',tags=['Integrations'])
@router.get('/google/connect')
def google_connect(current_user:UserResponse=Depends(get_current_user)):
    user_id=current_user.id
    auth_url=integration_service.start_google_oauth(user_id)
    return {'url':auth_url}

@router.get('/google/callback')
async def google_callback(
    code:str=Query(default=None),
    state:str=Query(...),
    error:str|None=Query(default=None),
    db:Session=Depends(get_db)):
    if error:
        raise HTTPException(
            status_code=400,
            detail=f'Google Authorization failed:{error}'
        )
    if not code:
        raise HTTPException (status_code=400,detail='Missing Authorization Code')
    try:
        return await integration_service.finish_google_oauth(
        code=code,
        state=state,
        db=db
        )
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
