from uuid import UUID

from sqlalchemy.orm import Session

from app.integrations.google.auth import GoogleAuth
from app.integrations.google.scopes_config import GOOGLE_APP_SCOPES
from app.integrations.google.state_store import state_store
from app.repositories.integration_installation_repo import IntegrationInstallationRepo
from app.repositories.integration_repo import IntegrationRepo


INTEGRATION_LABELS = {
    "google_sheets": "Google Sheets",
    "google_drive": "Google Drive",
    "google_docs": "Google Docs",
}


class IntegrationService:
    def __init__(self, google_auth, integration_repo, installation_repo):
        self.google_auth = google_auth
        self.integration_repo = integration_repo
        self.installation_repo = installation_repo

    def catalog(self) -> list[dict]:
        # The same scope registry drives both OAuth requests and frontend app discovery.
        return [
            {
                "key": key,
                "provider": "google",
                "name": INTEGRATION_LABELS.get(key, key),
                "scopes": scopes,
            }
            for key, scopes in GOOGLE_APP_SCOPES.items()
        ]

    def start_google_oauth(self, user_id: UUID, integration_key: str) -> str:
        scopes = GOOGLE_APP_SCOPES.get(integration_key)
        if scopes is None:
            raise ValueError(f"Unsupported Google integration: {integration_key}")
        return self.google_auth.get_authorization_url(user_id, integration_key, scopes)

    def list_user_integrations(self, user_id: UUID, db: Session) -> list[dict]:
        # Keep unconnected apps in the response so frontend lists have a stable shape.
        installations = {
            installation.integration_key: (connection, installation)
            for connection, installation in self.installation_repo.list_for_user(user_id, db)
        }
        result = []
        for item in self.catalog():
            pair = installations.get(item["key"])
            connection, installation = pair if pair else (None, None)
            result.append({
                **item,
                "connected": bool(installation and installation.status == "connected"),
                "enabled": bool(installation and installation.enabled and installation.status == "connected"),
                "status": installation.status if installation else "not_connected",
                "granted_scopes": installation.granted_scopes if installation else [],
                "last_connected_at": installation.last_connected_at if installation else None,
                "provider_connected": connection is not None,
            })
        return result

    def set_enabled(self, user_id: UUID, integration_key: str, enabled: bool, db: Session) -> dict:
        if integration_key not in GOOGLE_APP_SCOPES:
            raise ValueError(f"Unsupported Google integration: {integration_key}")
        pair = self.installation_repo.get_for_user(user_id, integration_key, db)
        if pair is None:
            raise ValueError("Integration is not connected")
        _, installation = pair
        self.installation_repo.set_enabled(installation, enabled)
        db.commit()
        return {
            "key": integration_key,
            "enabled": bool(enabled),
            "status": installation.status,
        }

    def disconnect(self, user_id: UUID, integration_key: str, db: Session) -> dict:
        return self.set_enabled(user_id, integration_key, False, db)

    def finish_google_oauth(self, code: str, state: str, db: Session) -> dict:
        # One-time Redis state carries the trusted account/app context through Google's redirect.
        ctx = self.google_auth.consume_state(state)
        user_id = ctx["user_id"]
        integration_key = ctx["integration_key"]
        requested_scopes = ctx["scopes"]
        if integration_key not in GOOGLE_APP_SCOPES:
            raise ValueError("OAuth state contains an unsupported integration")

        credentials = self.google_auth.exchange_code(
            code=code,
            state=state,
            code_verifier=ctx["code_verifier"],
            # Pass the scopes saved with OAuth state; the callback must use the same app scope set.
            scopes=requested_scopes,
        )
        # Incremental consent may omit refresh_token; retain the user's existing refresh token.
        existing = self.integration_repo.get_google_connection(user_id=user_id, db=db)
        refresh_token = credentials.refresh_token or (existing.refresh_token if existing else None)
        access_token = credentials.token or (existing.access_token if existing else None)
        if not refresh_token:
            raise ValueError("Google did not return a refresh token. Revoke the existing Google app grant and reconnect.")

        # Google can omit `scope` from a successful token response, so retain the consented request as fallback.
        granted_scopes = (
            getattr(credentials, "granted_scopes", None)
            or getattr(credentials, "scopes", None)
            or requested_scopes
        )
        if not granted_scopes:
            raise ValueError("Google did not return the granted scopes; the integration was not saved")
        # OAuthlib now accepts Google's extra identity scopes, but the selected app must retain every required scope.
        if not set(requested_scopes).issubset(set(granted_scopes)):
            raise ValueError("Google did not grant every permission required by this integration")

        # Persist shared provider credentials and the app installation in one transaction.
        try:
            connection = self.integration_repo.save_google_connection(
                user_id=user_id,
                refresh_token=refresh_token,
                access_token=access_token,
                expires_at=credentials.expiry,
                db=db,
            )
            self.installation_repo.save_installation(
                integration_id=connection.id,
                integration_key=integration_key,
                requested_scopes=requested_scopes,
                granted_scopes=list(granted_scopes),
                db=db,
            )
            db.commit()
        except Exception:
            db.rollback()
            raise

        return {"message": "Google account connected", "integration_key": integration_key}


integration_service = IntegrationService(
    google_auth=GoogleAuth(state_store),
    integration_repo=IntegrationRepo(),
    installation_repo=IntegrationInstallationRepo(),
)
