tools=[
    {
        "type": "function",
        'function': {
            'name': 'add',
            'description': 'Add two numbers',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'number', 'description': 'First number to add'},
                    'b': {'type': 'number', 'description': 'Second number to add'}
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
                    'a': {'type': 'number', 'description': 'First number to multiply'},
                    'b': {'type': 'number', 'description': 'Second number to multiply'}
                }
            }
        }

    }
]