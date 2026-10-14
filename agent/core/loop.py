from agent.config import settings
from agent.tools.registry import tools_registry
from agent.models import LLMRequestModel, Message ,AssistantMessage, ToolMessage
from agent.core.dispatcher import execute_tool
from agent.core.llm import LLM
from agent.utils.logger import get_logger

logger=get_logger(__name__)

def run_agent(message:list[Message],llm:LLM):
    logger.info(f'Conversation History:{message}')
    tool_schemas=[entry['schema'] for entry in tools_registry.values()]
    for step in range(settings.agent.MAX_STEPS):
        request=LLMRequestModel(
            message_request=message,
            tools=tool_schemas
        )
        assistant_message=llm.call_llm(llm_request=request)

        message.append(AssistantMessage(
                content=assistant_message.content,
                tool_call=assistant_message.tool_calls
            ))
        if not assistant_message.tool_calls:
            resp=assistant_message.content
            # logger.info(f'Response From Model:{resp}')

            return resp
        else:
            
            #----------------------Tool Dispatch-----------------------------
            for tc in assistant_message.tool_calls:
                result=execute_tool(tc)
                message.append(ToolMessage(
                    tool_call_id=tc.id,
                    content=str(result),
                ))
        