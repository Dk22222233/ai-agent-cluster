import uuid
from app.models import MessageModel
from app.api.dependencies import get_db
class MessageRepo:
    def __init__(self,db):
        self.db=db

    def create_msg(self,conversation_id:uuid.UUID,role:str,content:str,tool_calls,tool_call_id)->MessageModel:
        msg_orm=MessageModel(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_call_id=tool_call_id
        )
        self.db.add(msg_orm)
        self.db.commit()
        self.db.refresh(msg_orm)
        return msg_orm

    def get_latest(self,conversation_id:uuid.UUID,n:int):
        pass

message_repo=MessageRepo(get_db())

