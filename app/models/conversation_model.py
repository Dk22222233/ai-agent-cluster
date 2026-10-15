from app.infrastructure.database.connection import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy import String, DateTime, func, ForeignKey
from datetime import datetime
from app.models.message_model import MessageModel
from sqlalchemy.dialects.postgresql import UUID
class ConversationModel(Base):
    __tablename__='conversation'
    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default= uuid.uuid4)

    #---show ownership of conversation using authenticated user id
    user_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False, 
    index=True,
    )

    title:Mapped[str|None]=mapped_column(String(200),nullable=True)

    created_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
        )

    updated_at:Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
        )

    message:Mapped[list["MessageModel"]]=relationship(
        back_populates='conversation',
        cascade='all, delete-orphan',
        order_by='MessageModel.created_at'
    )