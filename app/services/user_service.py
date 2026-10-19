from app.api.schemas.user_schema import UserResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories import user_repo
class UserService:
    def create_user(self, user:UserResponse,db:Session)->UserResponse:
        existing=user_repo.get_user_by_id(user=user,db=db)
        if existing is not None:
            return UserResponse(
                id=existing.id,
                name=existing.name,
                email=existing.email
            )
        try:
            user_orm=user_repo.create_user(user,db)
            return UserResponse(
                id=user_orm.id,
                name=user_orm.name,
                email=user_orm.email
            )
        
        except IntegrityError:
            db.rollback()
            existing=user_repo.get_user_by_id(user=user,db=db)
            if existing is None:
                raise 
            return UserResponse(
                id=existing.id,
                name=existing.name,
                email=existing.email
            )
user_service=UserService()