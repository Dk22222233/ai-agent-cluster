from agent.tools.registry import tools_registry
from agent.core.validator import validate_args
import json
from agent.utils.logger import get_logger
logger=get_logger(__name__)
def execute_tool(tool_call):
    try:
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
        return str(result)
    except Exception as e:
        logger.info(f'Error in tool call:{e}')
        return f'Tool error:{str(e)}'