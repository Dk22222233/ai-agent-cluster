from pydantic import BaseModel
class OAuthResponse(BaseModel):
    authorization_url:str
