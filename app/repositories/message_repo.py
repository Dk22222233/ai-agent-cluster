import uuid
from sqlalchemy.orm import Session
from app.models import MessageModel
from sqlalchemy import select
class MessageRepo:
    # def __init__(self,db:Session):
    #     self.db=db

    def create_msg(self,conversation_id:uuid.UUID,role:str,content:str,tool_calls,tool_call_id,db:Session)->MessageModel:
        msg_orm=MessageModel(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_call_id=tool_call_id
        )
        db.add(msg_orm)
        db.commit()
        db.refresh(msg_orm)
        return msg_orm

    def get_latest(self,conversation_id:uuid.UUID,n:int,db:Session)-> list[MessageModel]:
        '''
        Return the most recent `n` messages in the chronographical order'''
        stmt=(select(MessageModel).
              where(conversation_id==conversation_id).
              order_by(MessageModel.created_at._desc()).
              limit(n)
              )
        rows=list(db.execute(stmt).scalars().all())
        return list(reversed(rows))
message_repo=MessageRepo()

