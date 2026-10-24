from config import settings
from app.integrations.google.state_store import state_store
import os
from uuid import UUID
from google_auth_oauthlib.flow import Flow
import hashlib
import base64
import secrets
from datetime import datetime,timedelta, timezone

# Google may include previously granted OpenID scopes with an incremental app consent response.
# OAuthlib otherwise raises before we can validate that the selected app's scopes are still present.
os.environ.setdefault("OAUTHLIB_RELAX_TOKEN_SCOPE", "1")
SCOPES = [
    'openid',  # Add
    'https://www.googleapis.com/auth/userinfo.email',  # Add
    'https://www.googleapis.com/auth/userinfo.profile', # Add
    'https://www.googleapis.com/auth/spreadsheets',
]
class GoogleAuth:
    def __init__(self,state_store):
        self.state_store=state_store
        self.client_config={
            'web':{
                'client_id':settings.GOOGLE_CLIENT_ID,
                'client_secret':settings.GOOGLE_CLIENT_SECRET,
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://oauth2.googleapis.com/token",
                'redirect_uri':settings.GOOGLE_REDIRECT_URI,

            }
        }
    def get_authorization_url(self,user_id:UUID,integration_key:str,scopes:list[str])->str:
        # Request only the scopes configured for the selected integrated app.
        #built flow without a state
        flow=Flow.from_client_config(
            self.client_config,
            scopes=scopes,
            redirect_uri=settings.GOOGLE_REDIRECT_URI
        )
        # generate state and PKCE verifier
        # used to prevent CSRF attacks
        state=secrets.token_urlsafe(32)
        code_verifier=secrets.token_urlsafe(64)
        code_challenge = (base64.urlsafe_b64encode(
             hashlib.sha256(code_verifier.encode("ascii")).digest()
                ).rstrip(b"=").decode("ascii"))
        # save credentails to redis
        self.state_store.save(
            state=state,
            user_id=user_id,
            code_verifier=code_verifier,
            integration_key=integration_key,
            scopes=scopes,
            expires_at=datetime.now(timezone.utc)+timedelta(minutes=10)
        )
        # oauth url construction
        auth_url,_=flow.authorization_url(
            access_type="offline",
            prompt='consent',
            include_granted_scopes='true',
            state=state,
            code_challenge=code_challenge,
            code_challenge_method='S256'
        )
        return auth_url

    def consume_state(self,state:str)->dict:
        data=self.state_store.consume(state)
        if data is None:
            raise ValueError("Invalid, expire or already used OAuth state")
        return {
            'user_id':UUID(str(data['user_id'])),
            'code_verifier':str(data['code_verifier']),
            'integration_key':str(data['integration_key']),
            'scopes':list(data['scopes']),
        }

    def exchange_code(self, code: str, state: str, code_verifier: str, scopes: list[str]):
        # Reuse the app's requested scopes so credentials retain the consent context from authorization.
        flow=Flow.from_client_config(
            self.client_config,
            scopes=scopes,
            state=state
        )
        flow.redirect_uri=settings.GOOGLE_REDIRECT_URI
        flow.code_verifier=code_verifier
        flow.fetch_token(code=code)
        return flow.credentials
