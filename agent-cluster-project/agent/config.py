from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import BaseModel
class LLMSettings(BaseModel):
    MODEL_NAME:str='qwen3:0.6b'
    BASE_URL:str='http://localhost:11434/v1'
    API_KEY:str='ollama'

class AgentSettings(BaseModel):
    MAX_STEPS:int=10
    debug:bool=False
    
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file='.env',env_file_encoding='__',extra='ignore')
    llm:LLMSettings=LLMSettings()
    agent:AgentSettings=AgentSettings()
settings=Settings()