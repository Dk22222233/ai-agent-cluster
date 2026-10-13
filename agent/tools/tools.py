from pydantic import BaseModel, Field
class AddArgs(BaseModel):
    '''Add Two Numbers'''
    a:int = Field(description='First number to add')
    b:int = Field(description='second number to add')
def add(a:int, b:int):
    return a + b

class MulitplyArgs(BaseModel):
    '''Multiply two numbers'''
    a:int= Field(description='First number to multiply')
    b:int= Field(description='second number to multiply')
def multiply(a:int, b:int):
    return a * b