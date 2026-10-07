from pydantic import BaseModel, Field
from typing import Any
class LLMRequestModel(BaseModel):
    model:str
    message_request:list[dict]
    tools:list[dict]=Field(default_factory=list)
    parameters:dict[str,Any]=Field(default_factory=dict)