from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.integration_installation_model import IntegrationInstallationModel
from app.models.integration_model import IntegrationModel


class IntegrationInstallationRepo:
    # Rows track individual apps while sharing one provider connection per user.
    def list_for_user(self, user_id: UUID, db: Session) -> list[tuple[IntegrationModel, IntegrationInstallationModel]]:
        stmt = (
            select(IntegrationModel, IntegrationInstallationModel)
            .join(IntegrationInstallationModel, IntegrationInstallationModel.integration_id == IntegrationModel.id)
            .where(IntegrationModel.user_id == user_id)
            .order_by(IntegrationInstallationModel.integration_key)
        )
        return list(db.execute(stmt).all())

    def get_for_user(self, user_id: UUID, integration_key: str, db: Session):
        stmt = (
            select(IntegrationModel, IntegrationInstallationModel)
            .join(IntegrationInstallationModel, IntegrationInstallationModel.integration_id == IntegrationModel.id)
            .where(
                IntegrationModel.user_id == user_id,
                IntegrationInstallationModel.integration_key == integration_key,
            )
        )
        return db.execute(stmt).one_or_none()

    def save_installation(
        self,
        integration_id: UUID,
        integration_key: str,
        requested_scopes: list[str],
        granted_scopes: list[str],
        db: Session,
    ) -> IntegrationInstallationModel:
        stmt = select(IntegrationInstallationModel).where(
            IntegrationInstallationModel.integration_id == integration_id,
            IntegrationInstallationModel.integration_key == integration_key,
        )
        installation = db.execute(stmt).scalar_one_or_none()
        # Reconnection refreshes granted scopes and reactivates the existing installation.
        now = datetime.now(timezone.utc)
        if installation is None:
            installation = IntegrationInstallationModel(
                integration_id=integration_id,
                integration_key=integration_key,
                requested_scopes=requested_scopes,
                granted_scopes=granted_scopes,
                last_connected_at=now,
            )
            db.add(installation)
        else:
            installation.requested_scopes = requested_scopes
            installation.granted_scopes = granted_scopes
            installation.status = "connected"
            installation.enabled = True
            installation.last_connected_at = now
            installation.disconnected_at = None
        db.flush()
        return installation

    def set_enabled(self, installation: IntegrationInstallationModel, enabled: bool) -> None:
        # This changes local app availability without revoking the shared Google OAuth grant.
        installation.enabled = enabled
        if enabled:
            installation.status = "connected"
            installation.disconnected_at = None
        else:
            installation.status = "disconnected"
            installation.disconnected_at = datetime.now(timezone.utc)


integration_installation_repo = IntegrationInstallationRepo()
