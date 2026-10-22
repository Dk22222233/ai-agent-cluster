from agent.core.llm import LLM
from openai import OpenAI
import json
from agent.models import (
    ResponseModel, 
    Usage, 
    ToolCall,
    LLMRequestModel,
    UserMessage, 
    Message,
    SystemMessage,
    AssistantMessage,
    ToolMessage,
    ToolDefinition
    )

class OpenAIAdapter(LLM):
    def __init__(self,model_name, base_url,api_key):
        self.model_name=model_name
        self.base_url=base_url
        self.api_key=api_key
        self.client= OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        # ---covert agent standard messages into openAI compatible 
    def _to_openAI_messages(self,messages:list[Message])->list[dict]:
        output:list[dict]=[]
        for m in messages:
            if isinstance(m,SystemMessage):
                output.append({
                    'role':'system',
                    'content':m.content
                })
            elif isinstance(m, UserMessage):
                output.append({"role": "user", "content": m.content})
            elif isinstance(m,AssistantMessage):
                d:dict={
                    'role':'assistant',
                    'content':m.content or ''
                }
                if m.tool_calls:
                    d["tool_calls"]=[
                        {
                        'id':tc.id,
                        'type':'function',
                        'function':{
                            'name':tc.name,
                            'arguments':json.dumps(tc.arguments)
                        }
                    }
                     for tc in m.tool_calls
                    ]
                output.append(d)
            elif isinstance(m,ToolMessage):
                output.append({
                    'role':'tool',
                    'tool_call_id':m.tool_call_id,
                    'content':m.content
                })

            else:
                raise TypeError(f'Unknown message type: {type(m)}')

        return output
    def _to_openAI_tools(self, tools: list[ToolDefinition]) -> list[dict]:
        return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            },
        }
        for tool in tools
    ]
    def _to_tool_call_model(self,raw):
        if not raw:
            return []
        return [
            ToolCall(
                id=tc.id,
                name=tc.function.name,
                arguments=json.loads(tc.function.arguments)
            )
            for tc in raw
        ]
    # this is request model a request model just take request and design response acc to DTO
    def call_llm(self, llm_request:LLMRequestModel)->ResponseModel:
        kwargs={
            'model':self.model_name,
            'messages':self._to_openAI_messages(llm_request.message_request)
        }
        # ------pick tools from request and convert it into llm specific
        tools=self._to_openAI_tools(llm_request.tools)
        if tools:
            kwargs['tools']=tools

        response = self.client.chat.completions.create(**kwargs)
        choice = response.choices[0]

        return ResponseModel(
            id=response.id,
            content=choice.message.content,
            tool_calls=self._to_tool_call_model(choice.message.tool_calls),
            finish_reason=choice.finish_reason,        
            model=response.model,
            usage=Usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
         ),
)

    