from auth.providers.supabase import SupabaseAuthProvider
from auth.interface import AuthProvider
class AuthService:
    def __init__(self,provider:AuthProvider):
        self.provider = provider
    def get_user(self,access_token):
        return self.provider.get_user(access_token)

auth_service = AuthService(SupabaseAuthProvider()) 