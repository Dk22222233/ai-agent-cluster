from app.api.schemas import AgentChatResponse, AgentChatRequest
from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.api.schemas import UserResponse
from app.services import agent_service
router=APIRouter(prefix='/agent',tags=['Agent'])

@router.post('/chat') #,response_model=AgentChatResponse
def agent_chat_request(request:AgentChatRequest): # , user:UserResponse=Depends(get_current_user)
    input_request=request.message
    resp=agent_service.agent_chat_request_service(input_request)
    return {
        'Model Response':resp
    }

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
