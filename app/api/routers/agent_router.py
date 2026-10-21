from app.api.schemas import AgentChatResponse, AgentChatRequest
from fastapi import APIRouter, Depends
import uuid
from app.api.dependencies import get_current_user, get_db
from app.api.schemas import UserResponse
from app.services import agent_service
from sqlalchemy.orm import Session
router=APIRouter(prefix='/agent',tags=['Agent'])

@router.post('/chat',response_model=AgentChatResponse) 
def agent_chat_request(request:AgentChatRequest,db:Session=Depends(get_db), user:UserResponse=Depends(get_current_user) ):  #
    user_id=user.id
    resp=agent_service.agent_chat_request_service(request,user_id,db)
    return resp
@router.post('/chat/stream')
def agent_chat_streaming():
    pass

@router.get('/conversations')
def agent_conversations():
    pass

@router.get('/conversation/{conversation_id}')
def get_specific_conversation():
    pass

@router.delete('/conversation/{conversation_id}')
def delete_specific_conversation():
    pass
