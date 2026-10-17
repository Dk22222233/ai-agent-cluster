from pydantic import BaseModel
from .message_model import AssistantMessage, Message
from .response_model import Usage
class AgentResult(BaseModel):
    '''Final Response to the user, For Public Use `Output of agent_runtime`
    - `new_message`: every msg in this run, appended except usermsg, initial sysprmpt and prior hist 
    '''
    message:AssistantMessage
    new_messages:list[Message]=[]
    steps:int=0
    finish_reason:str |None=None
    usage:Usage|None=None
    error:str |None=None