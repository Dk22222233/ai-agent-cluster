"""
The boundary between app-level ORM rows and agent-level DTOs.

This is the ONLY module in app/ that imports both sides. Everything
else speaks one language. Translation is symmetric:
    orm_to_agent_messages    : MessageModel[]   → Message[]
    agent_message_to_orm_fields : AssistantMessage → dict (ORM columns)
"""
from agent import (Message,AssistantMessage,ToolMessage,SystemMessage, UserMessage, ToolCall)
from app.models import MessageModel
from agent import get_logger, AgentResult

logger= get_logger(__name__)
def _orm_to_agent_dto(rows:list[MessageModel])->list[Message]:
    '''
    This function convert each db row into agent native Message
    '''
    output:list[Message]=[]
    for row in rows:
        content=row.content
        role=row.role
        tool_calls=row.tool_calls
        tool_call_id=row.tool_call_id

        if role == 'user':
            user_msg=UserMessage(
                role='user',
                content=content 
            )
            output.append(user_msg)

        if role=='assistant':
            assistant_msg=AssistantMessage(
                role='assistant',
                content=content or '', # pasres tool_calls to matching formate
                tool_calls=_parse_tool_calls(tool_calls) or []
            )
            output.append(assistant_msg)

        if role=='system':
            sys_msg=SystemMessage(
                role='system',
                content=content
            )
            output.append(sys_msg)

        if role=='tool':
            if not tool_call_id:
                logger.warning(f'No tool_call_id found for row.id:{row.id}')
                continue
            tool_msg=ToolMessage(
                role='tool',
                tool_call_id=tool_call_id,
                content=content
            )
            output.append(tool_msg)

    return output
# we should convert raw jsonb to list[ToolCall] as Message only require list[ToolCall] for agent
def _parse_tool_calls(raw:list|None)->list[ToolCall]|None:
    '''JSONB ---->> list[Message]'''
    if not raw:
        return None
    try: 
        return [ToolCall.model_validate(tc) for tc in raw]
    except Exception:
        ValueError('Malformed tool_calls JSONB dropping')
        return None

def _message_dto_to_orm(message:Message)->dict:
    '''
    Convert Agent output (AgentResult) to ORM for db compatability
    '''
    

    if isinstance(message,UserMessage):
        return {
            'role':'user',
            'content':message.content,
            'tool_calls':None,
            'tool_call_id':None
        }

    if isinstance(message,SystemMessage):
        return {
            'role':'system',
            'content':message.content,
            'tool_calls':None,
            'tool_call_id':None
        }

    if isinstance(message,AssistantMessage):
        return {
            'role':'assistant',
            'content':message.content,
            'tool_calls':(
                [tc.model_dump() for tc in message.tool_calls]
                if message.tool_calls else None
            ),
            'tool_call_id':None
        }
    if isinstance(message,ToolMessage):
        return {
            'role':'tool',
            'content':message.content,
            'tool_calls':None,
            'tool_call_id':message.tool_call_id
        } 