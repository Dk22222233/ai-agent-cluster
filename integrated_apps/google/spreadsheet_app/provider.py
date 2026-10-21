from app.integrations.google.credentials import GoogleCredentialFactory
from integrated_apps.google.spreadsheet_app.spreadsheet_service import (
    SpreadsheetService,
)


def build_spreadsheet_service(ctx) -> SpreadsheetService:
    credential_factory = GoogleCredentialFactory(
        db=ctx.db,
        user_id=ctx.user_id,
    )

    return SpreadsheetService(
        credential_factory=credential_factory,
    )