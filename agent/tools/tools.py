from pydantic import BaseModel, Field
class Add(BaseModel):
    '''Add Two Numbers'''
    a:int = Field(description='First number to add')
    b:int = Field(description='second number to add')
def add(a:int, b:int):
    return a + b

class Mulitply(BaseModel):
    '''Multiply two numbers'''
    a:int= Field(description='First number to multiply')
    b:int= Field(description='second number to multiply')
def multiply(a:int, b:int):
    return a * b