from .tools import add, multiply, AddArgs, MulitplyArgs

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