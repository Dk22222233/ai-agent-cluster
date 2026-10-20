from pydantic import BaseModel, Field
from agent.models.message_model import Message
from typing import Any
class LLMRequestModel(BaseModel):
    # model:str
    message_request:list[Message]
    tools:list[ToolDefinition]=Field(default_factory=list)
    parameters:dict[str,Any]=Field(default_factory=dict)

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]