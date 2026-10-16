from pydantic import BaseModel
from .message_model import AssistantMessage
from .response_model import Usage
class AgentResult(BaseModel):
    '''Final Response to the user, For Public Use `Output of agent_runtime`'''
    message:AssistantMessage
    steps:int=0
    finish_reason:str |None=None
    usage:Usage|None=None
    error:str |None=None
