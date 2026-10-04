# from core.llm import LLM
from agent.core.loop import run_agent
from inputs import input_message
from utils.logger import get_logger
logger=get_logger(__name__)
# llm1=LLM('qwen3:0.6b','http://localhost:11434/v1','ollama')
inputs=input_message(user_input="hey add and multiple 9 and 6 and then add the result of both")

agent_resp=run_agent(inputs)
logger.info(f"Response from LLM: {agent_resp}")