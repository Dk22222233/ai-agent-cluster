import uuid
from app.api.dependencies import get_db
class MessageRepo:
    def __init__(self,db):
        self.db=db

    def create_msg(self,conversation_id:uuid.UUID,role:str,content:str):
        pass

    def get_latest(self,conversation_id:uuid.UUID,n:int):
        pass

message_repo=MessageRepo(get_db())

