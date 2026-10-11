from sqlalchemy import String, DateTime, func
from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.connection import Base
class UserModel(Base):
    __tablename__='users'
    id:Mapped[uuid.UUID]=mapped_column(primary_key=True, nullable=False)
    name:Mapped[str|None]=mapped_column(String(100))
    email:Mapped[str]=mapped_column(String(255), unique=True,index=True,nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)