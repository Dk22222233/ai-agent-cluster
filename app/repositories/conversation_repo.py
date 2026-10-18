import uuid
from sqlalchemy.orm import Session
from app.models import ConversationModel
from sqlalchemy import select
class ConversationRepo:
    # def __init__(self):
    #     pass

    def create_for_user(self,title:str,user_id:uuid.UUID,db:Session)->ConversationModel:
        conv=ConversationModel(
            user_id=user_id,
            title=title
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)
        return conv
    #-----------enfore user ownership and get only selected by specific user
    def get_chat_by_id_for_user(self, conversation_id:uuid.UUID,user_id:uuid.UUID,db:Session)->ConversationModel|None:
        stmt=select(ConversationModel).where(
            ConversationModel.user_id==user_id, ConversationModel.id==conversation_id
        )
        return db.execute(stmt).scalar_one_or_none()
    #-------pick user specific selected chat and delete it and return True signal on deletion
    def delete_by_id_for_user(self,conversation_id:uuid.UUID,user_id:uuid.UUID,db:Session)->bool:
        chat=self.get_chat_by_id_for_user(conversation_id=conversation_id,user_id=user_id)
        db.delete(chat)
        db.commit()
        return True
        
    def update_title(self,conversation_id:uuid.UUID):
        pass
conversation_repo=ConversationRepo()