import uuid
from app.api.dependencies import get_db
from app.models import ConversationModel
from sqlalchemy import select
class ConversationRepo:
    def __init__(self,db):
        self.db=db

    def create_for_user(self,title:str,user_id:uuid.UUID)->ConversationModel:
        conv=ConversationModel(
            user_id=user_id,
            title=title
        )
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv
    #-----------enfore user ownership and get only selected by specific user
    def get_chat_by_id_for_user(self, conversation_id:uuid.UUID,user_id:uuid.UUID)->ConversationModel|None:
        stmt=select(ConversationModel).where(
            ConversationModel.user_id==user_id and ConversationModel.id==conversation_id
        )
        return self.db.execute(stmt).scalar_one_or_none()
    #-------pick user specific selected chat and delete it and return True signal on deletion
    def delete_by_id_for_user(self,conversation_id:uuid.UUID,user_id:uuid.UUID)->bool:
        chat=self.get_chat_by_id_for_user(conversation_id=conversation_id,user_id=user_id)
        self.db.delete(chat)
        self.db.commit()
        return True
        
    def update_title(self,conversation_id:uuid.UUID):
        pass
conversation_repo=ConversationRepo(get_db())