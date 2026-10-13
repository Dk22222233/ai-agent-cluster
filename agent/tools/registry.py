from .tools import add, multiply, Add, Mulitply

tools_registry={
    'add':{
        'function':add,
        'schema':Add
    },
    'multiply':{
        'function':multiply,
        'schema':Mulitply
    }
}