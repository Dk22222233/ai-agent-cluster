from agent.config import settings
from agent.core.model_adapters.openai_adapter import OpenAIAdapter
from agent.tools.schemas import tools
from agent.core.dispatcher import execute_tool
from agent.core.llm import LLM
from agent.utils.logger import get_logger

logger=get_logger(__name__)

def run_agent(message:list[dict]):
    llm=OpenAIAdapter(model_name=settings.llm.MODEL_NAME,base_url=settings.llm.BASE_URL,api_key=settings.llm.API_KEY)
    for step in range(settings.agent.MAX_STEPS):
        assistant_message=llm.call_llm(message,tools=tools)
        if not assistant_message.tool_calls:
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
                            'name':tc.function.name,
                            'arguments':tc.function.arguments
                                }
                            }
                            for tc in assistant_message.tool_calls
                        ]
                    })
            #----------------------Tool Dispatch-----------------------------
            for tool_call in assistant_message.tool_calls:
                result=execute_tool(tool_call)
                message.append({
                    'role':'tool',
                    'tool_call_id':tool_call.id,
                    'content':str(result)
                })
