from pydantic import BaseModel , Field
from datetime import datetime
from uuid import UUID
#----------------------------------
            # Chat
#----------------------------------
class AgentChatRequest(BaseModel):
    message:str =Field(min_length=1)
    conversation_id:UUID |None=None

class AgentChatResponse(BaseModel):
    conversation_id:UUID |None=None # make it normal when working on production system
    response:MessageResponse

#----------------------------------
        # Conversation
#----------------------------------

class ConversationResponse(BaseModel):
    id: UUID
    title: str | None = None
    created_at: datetime
    updated_at: datetime

#----------------------------------
        # Messages
#----------------------------------
class MessageResponse(BaseModel):
    id:UUID
    role:str
    content:str
#----------------------------------
        # Agent Configurations
#----------------------------------
class AgentCreateRequest(BaseModel):
    name:str
    model:str
    instructions:str
    tools:list[str]

class AgentResponse(BaseModel):
    id:UUID
    name:str
    model:str
    instructions:str
    tools:list[str]
