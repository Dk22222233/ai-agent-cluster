# provider.py
from app.integrations.google.credentials import GoogleCredentialFactory
from integrated_apps.google.spreadsheet_app.spreadsheet_service import (
    SpreadsheetService,
)


def build_spreadsheet_service(ctx) -> SpreadsheetService:
    credential_factory = GoogleCredentialFactory(
        db=ctx.db,
        # Match tool availability to the user's enabled Sheets installation.
        integration_key="google_sheets",
        # user_id=ctx.user_id,
    )

    return SpreadsheetService(
        credential_factory=credential_factory,
        # The service keeps request identity internally; handlers receive no user ID parameter.
        user_id=ctx.user_id,
    )
