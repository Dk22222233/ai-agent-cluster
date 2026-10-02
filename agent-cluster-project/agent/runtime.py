from core.llm import LLM
from inputs import input_message
from utils.logger import get_logger
logger=get_logger(__name__)
llm1=LLM('qwen3:0.6b','http://localhost:11434/v1','ollama')
inputs=input_message(user_input="Tell me a joke about programming.")
resp=llm1.call_llm(inputs)
logger.info(f"Response from LLM: {resp.message.content}")