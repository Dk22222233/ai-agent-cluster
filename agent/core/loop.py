from agent.config import settings
from agent.tools.schemas import tools
import json
from agent.core.llm import LLM
from agent.utils.logger import get_logger
from agent.tools.registry import tools_registry
from agent.core.validator import validate_args
logger=get_logger(__name__)

def run_agent(message:list[dict]):
    llm=LLM(model_name=settings.llm.MODEL_NAME,base_url=settings.llm.BASE_URL,api_key=settings.llm.API_KEY)
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
                name=tool_call.function.name # this get the function name from the ai response
                logger.info(f'Tool Name:{name}')
                tool=tools_registry[name] # pick a tool from available (tool registry) tools
                logger.info(f'Tool Picked From Registry:{tool}')
                args_schema=tool['schema'] # access schema for specific tool from avavilable tools (tool registry)
                logger.info(f'Access Args Schema From Registry:{args_schema}')
                function=tool['function'] # fxn of tool accessed 
                arguments=json.loads(tool_call.function.arguments) # llm generated tool arguments
                validated_args=validate_args(args_schema,arguments) # this fxn compare my base model(schema) with ai generated tool args
                result=function(**validated_args.model_dump()) # model dump is used to convert base model schema to py dict
                logger.info(f'tool result: {result}')
                message.append({
                    'role':'tool',
                    'tool_call_id':tool_call.id,
                    'content':str(result)
                })
