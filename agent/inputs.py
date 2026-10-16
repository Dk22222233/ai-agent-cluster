from agent.core.prompts import SYSTEM_PROMPT, ERROR_PROMPT
from agent.models import Message, SystemMessage,AssistantMessage, UserMessage
def input_message(user_input:str, history:list[Message]|None=None)->list[Message]:
    message:list[Message]=[
        SystemMessage(role='system',content=SYSTEM_PROMPT+ERROR_PROMPT)
    ]
    if history:
        message.extend(history)
    message.append(
        UserMessage(
            role='user',
            content=user_input
        )
    )
    return message
