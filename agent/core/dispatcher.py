from agent.tools.registry import tools_registry
from agent.models.response_model import ToolCall
from agent.utils.logger import get_logger
logger=get_logger(__name__)
def execute_tool(tool_call:ToolCall):
    try:
        name=tool_call.name # this gets the function name from the ai response stored in DTO ResponseModel
        logger.debug(f'Tool Name:{name}')

        tool=tools_registry[name] # pick a tool from available (tool registry) tools
        logger.debug(f'Tool Picked From Registry:{tool}')

        args_schema=tool['schema'] # access schema for specific tool from avavilable tools (tool registry)
        logger.debug(f'Access Args Schema From Registry:{args_schema}')

        function=tool['function'] # fxn of tool accessed 

        arguments=tool_call.arguments # llm generated tool arguments parsed by adapter

        validated_args=args_schema.model_validate(arguments) # this fxn compare my base model(schema) with ai generated tool args
        result=function(**validated_args.model_dump()) # model dump is used to convert base model schema to py dict
        logger.info(f"Tool {name}({tool_call.arguments}) → {result}")
        
        return str(result)
    except Exception as e:
        logger.info(f'Error in tool call:{e}')
        return f'Tool error:{str(e)}'