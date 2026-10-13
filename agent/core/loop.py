from agent.config import settings
from agent.tools.registry import tools_registry
from agent.models.llm_request_model import LLMRequestModel
from agent.core.dispatcher import execute_tool
from agent.core.llm import LLM
from agent.utils.logger import get_logger

logger=get_logger(__name__)

def run_agent(message:list[dict],llm:LLM):
    tool_schemas=[entry['schema'] for entry in tools_registry.values()]
    for step in range(settings.agent.MAX_STEPS):
        request=LLMRequestModel(
            message_request=message,
            tools=tool_schemas
        )
        assistant_message=llm.call_llm(llm_request=request)
        if not assistant_message.tool_call:
            resp=assistant_message.content
            logger.info(f'Response From Model:{resp}')
            return resp
        else:
            message.append({
                'role':'assistant',
                'tool_calls':[
                    {
                        'id':tc.id,
                        'type':'function',
                        'function':{
                            'name':tc.name,
                            'arguments':tc.arguments
                                }
                            }
                            for tc in assistant_message.tool_call
                        ]
                    })
            #----------------------Tool Dispatch-----------------------------
            for tc in assistant_message.tool_call:
                result=execute_tool(tc)
                message.append({
                    'role':'tool',
                    'tool_call_id':tc.id,
                    'content':str(result)
                })
