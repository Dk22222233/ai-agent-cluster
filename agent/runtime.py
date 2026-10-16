# from core.llm import LLM
from agent.core.loop import run_agent
from agent.inputs import input_message
from agent.utils.logger import get_logger
from agent.config import settings
from agent import AgentResult, Message
from agent.core.model_adapters.openai_adapter import OpenAIAdapter
from agent.core.llm import LLM
logger=get_logger(__name__)

llm=OpenAIAdapter(model_name=settings.llm.MODEL_NAME,base_url=settings.llm.BASE_URL,api_key=settings.llm.API_KEY)

def agent_runtime(input:str, history:list[Message])->AgentResult:
  
    inputs=input_message(user_input=input,history=history)
    agent_resp=run_agent(inputs,llm)
    # logger.info(f"Response from LLM: {agent_resp}")
    return agent_resp