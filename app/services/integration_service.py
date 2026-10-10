from app.integrations.google.auth import GoogleAuth
from app.repositories.integration_repo import IntegrationRepo
class IntegrationService:
    def __init__ (self):
        self.google_auth=GoogleAuth()
        self.integration_repo=IntegrationRepo()
    def start_google_oauth(user_id):
        pass
def finish_google_oauth(self, code:str,state:str):
    user_id=self.goole_auth.consume_state(state)

    credentails=self.google_auth_.exchange_code(
        code=code,
        state=state
    )
    if not credentails.refresh_token:
        raise ValueError(
            "Google didn't return a refresh token"
            'Handle the existing connection or reauthorization'
        )
    self.integration_repo.save_google_connection(
        user_id=user_id,
        refresh_token=credentails.refresh_token
    )
    return {
        'message':"Google Account Connected Successfully"
    }

integration_service=IntegrationService()