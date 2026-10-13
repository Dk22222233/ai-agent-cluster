from pydantic import BaseModel,Field
class ResponseModel(BaseModel):
    id:str
    content:str|None =None
    tool_call:list[ToolCall]
    finish_reason:str|None=None
    model:str|None=None
    raw:dict|None=Field(default=None,exclude=True)
    usage:Usage|None=None
    

class Usage(BaseModel):
    prompt_tokens:int
    completion_tokens:int
    total_tokens:int

class ToolCall(BaseModel):
    id:str
    name:str
    arguments:dict

