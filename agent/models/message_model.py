from pydantic import BaseModel
from typing import Literal
from agent.models.response_model import ToolCall

class AssistantMessage(BaseModel):
    role:Literal['assistant']
    content:str|None=None
    tool_call:list[ToolCall]|None=None

class SystemMessage(BaseModel):
    role:Literal['system']
    content:str

class UserMessage(BaseModel):
    role:Literal['user']
    content:str

class ToolMessage(BaseModel):
    role:Literal['tool']
    tool_call_id:str
    content:str

Message=AssistantMessage|UserMessage|ToolMessage|SystemMessage