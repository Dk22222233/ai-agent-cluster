from config import settings
from uuid import UUID
from google_auth_oauthlib.flow import Flow
import hashlib
import base64
import secrets
from datetime import datetime,timedelta, timezone
SCOPES=[
    'https://www.googleapis.com/auth/spreadsheets.readonly'
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
    def get_authorization_url(self,user_id:UUID)->str:
        #built flow without a state
        flow=Flow.from_client_config(
            self.client_config,
            scopes=SCOPES,
            
        )
        # generate state and PKCE verifier
        # used to prevent CSRF attacks
        state=secrets.token_urlsafe(32)
        code_verifier=secrets.token_urlsafe(64)
        code_challenge = (base64.urlsafe_b64encode(
             hashlib.sha256(code_verifier.encode("ascii")).digest()
                ).rstrip(b"=").decode("ascii"))
        self.state_store.save(
            state=state,
            user_id=user_id,
            code_verifier=code_verifier,
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

    def consume_state(self,state:str)->UUID:
        user_id=self.state_store.consume(state)
        if user_id is None:
            raise ValueError("Invalid, expire or already used OAuth state")
        return UUID(str(user_id))

    def exchange_code(self, code:str, state:str):
        flow=Flow.from_client_config(
            self.client_config,
            scopes= SCOPES,
            state=state
        )
        flow.redirect_uri=settings.GOOGLE_REDIRECT_URI
        flow.fetch_token(code=code)
        return flow.credentials