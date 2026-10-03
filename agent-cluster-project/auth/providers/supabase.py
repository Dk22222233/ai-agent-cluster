from supabase import create_client
from supabase_auth import UserResponse
from interface import AuthProvider
from config import settings
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
class SupabaseAuthProvider(AuthProvider):
    def get_user(self, access_token: str):
        response= supabase.auth.get_user(access_token)
        
        if not response or not response.user:
            raise Exception("Invalid access token") 
        else:
            user=response.user
            return UserResponse(
                id=user.id,
                name=user.user_metadata.get("name"),
                email=user.email
            )