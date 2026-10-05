from pydantic import BaseModel
from typing import Type
def validate_args(schema:Type[BaseModel],arguments):
    return schema.model_validate(arguments) # return schema I have made if validation worked
class AddArgs(BaseModel):
    a:int
    b:int
class MulitplyArgs(BaseModel):
    a:int
    b:int