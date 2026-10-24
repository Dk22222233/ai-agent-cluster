
# app/integrations/google/scope_config.py

GOOGLE_APP_SCOPES: dict[str, list[str]] = {
    "google_sheets": [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
    ],
    "google_drive": [
        "https://www.googleapis.com/auth/drive.metadata.readonly",
    ],
    "google_docs": [
        "https://www.googleapis.com/auth/documents.readonly",
    ],
}
