from pydantic import BaseModel , Field
from uuid import UUID
class AgentChatRequest(BaseModel):
    message:str
    conversation_id:UUID |None=None

class AgentChatResponse(BaseModel):
    conversation_id:UUID |None=None # make it normal when working on production system
    response:str

class ConversationResponse(BaseModel):
    id:UUID
    title:str

class MessageResponse(BaseModel):
    id:UUID
    role:str
    content:str

class AgentCreateRequest(BaseModel):
    name:str
    model:str
    instructions:str
    tools:list[str]

class AgentResponse(BaseModel):
    id:UUID
    name:str
    instructions:str
    tools:list[str]
