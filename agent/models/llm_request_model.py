from pydantic import BaseModel, Field
from agent.models.message_model import Message
from typing import Any
class LLMRequestModel(BaseModel):
    # model:str
    message_request:list[Message]
    tools:list[type[BaseModel]]=Field(default_factory=list)
    parameters:dict[str,Any]=Field(default_factory=dict)