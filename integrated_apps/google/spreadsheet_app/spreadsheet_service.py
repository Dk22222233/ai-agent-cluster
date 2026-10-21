
from uuid import UUID

from app.integrations.google.credentials import GoogleCredentialFactory
from integrated_apps.google.spreadsheet_app.sheet_client import (
    get_sheet_client,
)


class SpreadsheetService:
    def __init__(self, credential_factory: GoogleCredentialFactory):
        self.credential_factory = credential_factory

    def build_client(self, user_id: UUID):
        credentials = self.credential_factory.get_credentials(user_id)
        return get_sheet_client(credentials)