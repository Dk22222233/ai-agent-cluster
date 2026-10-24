
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    JSON,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class IntegrationInstallationModel(Base):
    __tablename__ = "integration_installations"

    __table_args__ = (
        UniqueConstraint(
            "integration_id",
            "integration_key",
            name="uq_connection_integration_app",
        ),
        CheckConstraint(
            "status IN ('connected', 'disconnected', 'error')",
            name="ck_integration_installation_status",
        ),
    )

    # Unique ID for this app installation
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    # References the shared provider connection in integrations
    integration_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("integrations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Examples: google_sheets, google_drive, google_docs
    integration_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # OAuth connection state for this particular app
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="connected",
        server_default="connected",
    )

    # User can disable the app without revoking Google OAuth
    enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    # Scopes requested for this app's OAuth flow
    requested_scopes: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    # Scopes actually granted and confirmed by Google
    granted_scopes: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    last_connected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    disconnected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
