from .tools import add, multiply
from agent.core.validator import AddArgs,MulitplyArgs
tools_registry={
    'add':{
        'function':add,
        'schema':AddArgs
    },
    'multiply':{
        'function':multiply,
        'schema':MulitplyArgs
    }
}