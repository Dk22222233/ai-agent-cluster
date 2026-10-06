tools=[
    {
        "type": "function",
        'function': {
            'name': 'add',
            'description': 'Add two numbers',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'number', 'description': 'First number'},
                    'b': {'type': 'number', 'description': 'Second number'}
                }
            }
        }

    },
    {
        "type": "function",
        'function': {
            'name': 'multiply',
            'description': 'Multiply two numbers',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'number', 'description': 'First number'},
                    'b': {'type': 'number', 'description': 'Second number'}
                }
            }
        }

    }
]