from uuid import UUID

from app.integrations.google.credentials import GoogleCredentialFactory
from integrated_apps.google.drive_app.drive_client import get_drive_client


class DriveService:
    def __init__(self, credential_factory: GoogleCredentialFactory, user_id: UUID):
        self.credential_factory = credential_factory
        # Identity stays inside the service layer rather than being exposed as a tool argument.
        self.user_id = user_id

    def build_client(self):
        # Credentials are resolved per authenticated user; no Google token is shared across users.
        return get_drive_client(self.credential_factory.get_credentials(self.user_id))

    @staticmethod
    def _file_fields() -> str:
        return "id,name,mimeType,description,parents,webViewLink,createdTime,modifiedTime,size,trashed,owners(displayName,emailAddress)"

    @staticmethod
    def _escape_query_value(value: str) -> str:
        # Escape Drive query string delimiters before adding user input to q expressions.
        return value.replace("\\", "\\\\").replace("'", "\\'")

    def list_files(
        self,
        page_size: int = 20,
        page_token: str | None = None,
        query: str | None = None,
        folder_id: str | None = None,
        order_by: str = "modifiedTime desc",
    ) -> dict:
        drive = self.build_client()
        filters = ["trashed = false"]
        if query:
            filters.append(f"name contains '{self._escape_query_value(query)}'")
        if folder_id:
            filters.append(f"'{self._escape_query_value(folder_id)}' in parents")

        # Request only fields the tools expose and return a bounded page for predictable LLM context.
        response = drive.files().list(
            q=" and ".join(filters),
            pageSize=page_size,
            pageToken=page_token,
            orderBy=order_by,
            fields=f"nextPageToken,incompleteSearch,files({self._file_fields()})",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        return {
            "files": response.get("files", []),
            "next_page_token": response.get("nextPageToken"),
            "incomplete_search": response.get("incompleteSearch", False),
        }

    def get_file(self, file_id: str) -> dict:
        drive = self.build_client()
        # Drive returns only metadata under the configured drive.metadata.readonly permission.
        return drive.files().get(
            fileId=file_id,
            fields=self._file_fields(),
            supportsAllDrives=True,
        ).execute()
