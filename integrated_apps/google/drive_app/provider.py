from app.integrations.google.credentials import GoogleCredentialFactory
from integrated_apps.google.drive_app.drive_service import DriveService


def build_drive_service(ctx) -> DriveService:
    # Bind the shared credential factory to the request's database session and Drive app key.
    credential_factory = GoogleCredentialFactory(db=ctx.db, integration_key="google_drive")
    # Bind authenticated identity once so all Drive tools use the request's user.
    return DriveService(credential_factory=credential_factory, user_id=ctx.user_id)
