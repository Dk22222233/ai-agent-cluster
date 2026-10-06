# from core.llm import LLM
from agent.core.loop import run_agent
from agent.inputs import input_message
from agent.utils.logger import get_logger
logger=get_logger(__name__)
inputs=input_message(user_input="hey add and multiple 9 and 6 and then add the results of both")

agent_resp=run_agent(inputs)
logger.info(f"Response from LLM: {agent_resp}")
