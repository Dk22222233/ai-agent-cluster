from app.infrastructure.database.connection import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from sqlalchemy import String, DateTime, func, ForeignKey, Text,CheckConstraint, Index
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.conversation_model import ConversationModel
    
class MessageModel(Base):
    __tablename__='messages'

    __table_args__=(
        CheckConstraint("role IN ('user','assistant','tool','system')",name='ck_message_role'),
        Index('idx_messages_conv_created', 'conversation_id','created_at'),
        CheckConstraint("status IN ('streaming','completed','failed','cancelled')",name='ck_message_status')
    )

    id:Mapped[uuid.UUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)

    conversation_id:Mapped[uuid.UUID]=mapped_column(
        UUID(as_uuid=True),
        ForeignKey('conversation.id',ondelete='CASCADE'),
        nullable=False
    )

    role:Mapped[str]=mapped_column(String(20),nullable=False)

    content:Mapped[str|None]=mapped_column(Text, nullable=True)

    tool_calls: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    tool_call_id: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="completed",
        server_default="completed",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    conversation: Mapped["ConversationModel"] = relationship(
        back_populates="messages",
    )