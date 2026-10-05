from abc import ABC, abstractmethod
class AuthProvider(ABC):
    @abstractmethod
    def get_user(self, access_token: str):
        pass