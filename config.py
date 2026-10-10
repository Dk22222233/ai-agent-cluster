from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='.env',env_file_encoding='utf-8',extra='ignore')
    SUPABASE_URL: str
    SUPABASE_KEY: SecretStr
    GOOGLE_CLIENT_ID:str
    GOOGLE_CLIENT_SECRET:SecretStr
    GOOGLE_REDIRECT_URI:str
settings = Settings()