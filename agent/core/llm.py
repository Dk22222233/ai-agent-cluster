from abc import ABC,abstractmethod
from agent.models.llm_request_model import LLMRequestModel
from agent.models.response_model import ResponseModel
class LLM:
   
    @abstractmethod    
    def call_llm(self,llm_request:LLMRequestModel)->ResponseModel:
        pass 