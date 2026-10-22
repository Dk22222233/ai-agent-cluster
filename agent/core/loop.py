from agent.config import settings
from agent.tools.registry import tools_registry
from agent.models import LLMRequestModel, Message ,AssistantMessage, ToolMessage, AgentResult,Usage,ToolDefinition
from agent.core.dispatcher import execute_tool
from agent.core.llm import LLM
from agent import ExecutionContext
from agent.utils.logger import get_logger

logger=get_logger(__name__)

def _merge_usage(a:Usage|None,b:Usage|None)->Usage|None:
    if a is None:
        return b
    if b is None:
        return a 
    return Usage(
        prompt_tokens=a.prompt_tokens+b.prompt_tokens,
        completion_tokens=a.completion_tokens+b.completion_tokens,
        total_tokens=a.total_tokens+b.total_tokens
    )


def run_agent(message:list[Message],llm:LLM,ctx:ExecutionContext)->AgentResult:

    logger.info(f'Conversation History:{message}')
    # accessing objects from tool registry, tools var required by llmrequestmodel
    tools = [tool.definition for tool in tools_registry.values()]
    last_assistant:AssistantMessage|None=None
    total_usage:Usage|None=None
    #----capture the initail len of message, everything after this will consider as new msg
    initial_len=len(message)

    for step in range(1,settings.agent.MAX_STEPS+1):
        # passing the tool registry to request llm
        #---preparing request for llm acc request model 
        request=LLMRequestModel(
            message_request=message,
            tools=tools
        )
        #and llm will respond with ResponseModel
        llm_response=llm.call_llm(llm_request=request)
        print(f"DEBUG: content={llm_response.content!r}")
        print(f"DEBUG: tool_calls={llm_response.tool_calls!r}")
        print(f"DEBUG: finish_reason={llm_response.finish_reason!r}")
        total_usage=_merge_usage(total_usage,llm_response.usage)

        
        last_assistant=AssistantMessage(
            role='assistant',
            content=llm_response.content,
            tool_calls=llm_response.tool_calls
        )
        message.append(last_assistant)

        if not llm_response.tool_calls:
            return AgentResult(
                message=last_assistant,
                new_messages=message[initial_len:],
                steps=step,
                finish_reason=llm_response.finish_reason or 'stop',
                usage=total_usage
            )
        else:
            #----------------------Tool Dispatch-----------------------------
            for tc in llm_response.tool_calls:
                result=execute_tool(tc,ctx)
                # building and appending the tool message by using id from ResponseModel(LLM) and result from executor 
                message.append(ToolMessage(
                    role='tool',
                    tool_call_id=tc.id,
                    content=str(result),
                ))
    logger.info('Max steps reached without final answer')
    return AgentResult(
        message=last_assistant or AssistantMessage(content=None),
        new_messages=message[initial_len:],
        steps=settings.agent.MAX_STEPS,
        finish_reason='max-steps',
        usage=total_usage
    )
        