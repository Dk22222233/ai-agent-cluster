from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import SecretStr
class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(env_file='.env',env_file_encoding='utf-8',extra='ignore')
    SUPABASE_URL: str
    SUPABASE_KEY: str
    GOOGLE_CLIENT_ID:str
    GOOGLE_CLIENT_SECRET:str
    GOOGLE_REDIRECT_URI:str
    REDIS_URL:str
    OAUTH_TOKEN_ENCRYPTION_KEY:str
    # OAuth completion redirects to the configured frontend origin.
    FRONTEND_URL: str = "http://localhost:5173"
settings = Settings()
