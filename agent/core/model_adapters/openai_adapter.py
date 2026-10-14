from agent.core.llm import LLM
from openai import OpenAI
import json
from agent.models import ResponseModel, Usage, ToolCall,LLMRequestModel, Message

class OpenAIAdapter(LLM):
    def __init__(self,model_name, base_url,api_key):
        self.model_name=model_name
        self.base_url=base_url
        self.api_key=api_key
        self.client= OpenAI(
            base_url=base_url,
            api_key=api_key
        )
    def _to_openAI_messages(self,messages:list[Message])->list[dict]:
        pass
    def _to_openAI_tools(self,tools):
        if not tools:
            return None
        return [
            {
                'type':'function',
                'function':{
                    'name':t.__name__.lower(),
                    'description':t.__doc__ or '',
                    # it will eat more token as it has extra titles..
                    'parameters':t.model_json_schema()
                }
            }
            for t in tools
            ]
    def _to_tool_call(self,raw):
        if not raw:
            return None
        return [
            ToolCall(
                id=tc.id,
                name=tc.function.name,
                arguments=json.loads(tc.function.arguments)
            )
            for tc in raw
        ]
    def call_llm(self, llm_request:LLMRequestModel)->ResponseModel:
        response=self.client.chat.completions.create(
            model=self.model_name,
            messages=llm_request.message_request,
            tools=self._to_openAI_tools(llm_request.tools)
        )
        choice=response.choices[0]
        return ResponseModel(
            id=response.id,
            content=choice.message.content,
            tool_call=self._to_tool_call(choice.message.tool_calls) or [],
            finish_reason=choice.finish_reason,
            model=response.model,
            usage=Usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens
            )
        )

    