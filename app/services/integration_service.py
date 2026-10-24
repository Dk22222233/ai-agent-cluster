from app.integrations.google.auth import GoogleAuth
from sqlalchemy.orm import Session
from app.integrations.google.state_store import state_store
from app.integrations.google.scopes_config import GOOGLE_APP_SCOPES     
from app.repositories.integration_repo import IntegrationRepo
class IntegrationService:
    def __init__ (self,google_auth,integration_repo):
        self.google_auth=google_auth
        self.integration_repo=integration_repo

    def start_google_oauth(self,user_id,integration_key:str):
        # validate the requested integration
        scopes=GOOGLE_APP_SCOPES.get(integration_key)
        if scopes is None:
            raise ValueError(f"Unsupported Google Integration:{integration_key}")
        # generate url
        auth_url=self.google_auth.get_authorization_url(user_id,integration_key,scopes)
        return auth_url
    
    async def finish_google_oauth(self, code:str,state:str,db:Session):
        ctx=self.google_auth.consume_state(state)
        user_id=ctx['user_id']
        integration_key = ctx["integration_key"]
        requested_scopes = ctx["scopes"]
        code_verifier=ctx['code_verifier']
        #exchange the code for tokens
        credentails=self.google_auth.exchange_code(
            code=code,
            state=state,
            code_verifier=code_verifier
        )
        existing= self.integration_repo.get_google_connection(user_id=user_id,db=db)
        refresh_token=credentails.refresh_token or (existing.refresh_token if existing else None)
        access_token=credentails.token or (existing.access_token if existing else None)


        if not refresh_token:
            raise ValueError(
                "Google didn't return a refresh token"
                'Handle the existing connection or reauthorization'
            )
        
        connection=self.integration_repo.save_google_connection(
            user_id=user_id,
            refresh_token=refresh_token,
            access_token=access_token,
            db=db
        )
        granted_scopes=getattr(
            credentails,
            'granted_scopes',
            None
        )
        if not granted_scopes:
            raise ValueError(f'Google actual granted scopes were not returned')

        self.integration_repo.save_installations(
            user_id=user_id,
            integration_id=connection.id,
            granted_scopes=granted_scopes,
            db=db
        )
        return {
        'message':"Google Account Connected Successfully",
        'integration_key':integration_key
        }

integration_service=IntegrationService(google_auth=GoogleAuth(state_store),integration_repo=IntegrationRepo())