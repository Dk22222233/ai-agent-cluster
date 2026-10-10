from app.integrations.google.auth import GoogleAuth
from sqlalchemy.orm import Session
from app.integrations.google.state_store import state_store     
from app.repositories.integration_repo import IntegrationRepo
class IntegrationService:
    def __init__ (self,google_auth,integration_repo):
        self.google_auth=google_auth
        self.integration_repo=integration_repo

    def start_google_oauth(self,user_id):
        auth_url=self.google_auth.get_authorization_url(user_id)
        return auth_url
    
    async def finish_google_oauth(self, code:str,state:str,db:Session):
        ctx=self.google_auth.consume_state(state)
        user_id=ctx['user_id']
        code_verifier=ctx['code_verifier']
        #exchange the code for tokens
        credentails=self.google_auth.exchange_code(
            code=code,
            state=state,
            code_verifier=code_verifier
        )
        existing=await self.integration_repo.get_google_connection(user_id,db)
        refresh_token=credentails.refresh_token or (existing.refresh_token if existing else None)
        if not refresh_token:
            raise ValueError(
                "Google didn't return a refresh token"
                'Handle the existing connection or reauthorization'
            )
        
        self.integration_repo.save_google_connection(
            user_id=user_id,
            refresh_token=credentails.refresh_token,
            db=db
        )
        return {
        'message':"Google Account Connected Successfully"
        }

integration_service=IntegrationService(google_auth=GoogleAuth(state_store),integration_repo=IntegrationRepo)