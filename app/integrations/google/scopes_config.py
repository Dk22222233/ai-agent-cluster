
# app/integrations/google/scope_config.py

GOOGLE_APP_SCOPES: dict[str, list[str]] = {
    "google_sheets": [
        # The agent exposes write operations, so the Sheets integration needs write access.
        "https://www.googleapis.com/auth/spreadsheets",
        # Spreadsheet discovery uses Drive files.list to find spreadsheet IDs and names.
        "https://www.googleapis.com/auth/drive.metadata.readonly",
    ],
    "google_drive": [
        "https://www.googleapis.com/auth/drive.metadata.readonly",
    ],
    "google_docs": [
        "https://www.googleapis.com/auth/documents.readonly",
    ],
}
