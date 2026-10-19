from app.infrastructure.database.connection import Base
from app.api.schemas.user_schema import UserResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user_model import UserModel
class UserRepo:
    def create_user(self,user:UserResponse,db:Session)->UserModel:
        user_orm=UserModel(
            id=user.id,
            name=user.name,
            email=user.email
        )
        db.add(user_orm)
        db.commit()
        db.refresh(user_orm)
        return user_orm

    def get_user_by_id(self,user:UserResponse,db:Session)->UserModel|None:
        stmt=select(UserModel).where(UserModel.id==user.id)
        return db.execute(stmt).scalar_one_or_none()

user_repo=UserRepo()