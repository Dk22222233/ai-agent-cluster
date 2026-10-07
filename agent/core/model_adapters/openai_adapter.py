from agent.core.llm import LLM
from openai import OpenAI
from agent.models.response_model import ResponseModel
from agent.models.llm_request_model import LLMRequestModel
class OpenAIAdapter(LLM):
    def __init__(self,model_name, base_url,api_key):
        self.model_name=model_name
        self.base_url=base_url
        self.api_key=api_key
        self.client= OpenAI(
            base_url=base_url,
            api_key=api_key
        )
    def call_llm(self, llm_request:LLMRequestModel)->ResponseModel:
        return ResponseModel