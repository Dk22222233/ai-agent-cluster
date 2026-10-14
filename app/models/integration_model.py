import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    JSON,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.connection import Base
class IntegrationModel(Base):
    __tablename__='integrations'
    __table_args__=(UniqueConstraint('user_id','provider',name='uq_integration_user_provider'),)
    # uniquue id for each integration connection
    id:Mapped[uuid.UUID]=mapped_column(primary_key=True,default=uuid.uuid4)
    # owner id: application user id  
    user_id:Mapped[uuid.UUID]=mapped_column(ForeignKey('users.id',ondelete='CASCADE'),nullable=False,index=True)

    provider:Mapped[str]=mapped_column(String(50),nullable=False)

    access_token:Mapped[str|None]=mapped_column(String,nullable=True)

    refresh_token:Mapped[str|None]=mapped_column(String,nullable=True)

    expires_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)

    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_onupdate=func.now(),onupdate=func.now(),nullable=False)