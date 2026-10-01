from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import BaseModel
class LLMSettings(BaseModel):
    model_name:str='qwen3:0.6b'
    base_url:str='http://localhost:11434/v1'
    api_key:str='ollama'

class AgentSettings(BaseModel):
    max_steps:int=10
    debug:bool=False
    
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file='.env',env_file_encoding='__',extra='ignore')
    llm:LLMSettings=LLMSettings()
    agent:AgentSettings=AgentSettings()