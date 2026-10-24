# Integrated apps API

The API stores one encrypted Google OAuth connection per user in `integrations`. Each supported app (Sheets, Drive, Docs) has its own row in `integration_installations`, including its granted scopes and enabled state. OAuth state is kept in Redis for ten minutes and is consumed once by the callback.

Before deploying this change, apply `migrations/20261024_create_integration_installations.sql` to the PostgreSQL database. Set `FRONTEND_URL` to the frontend origin used for the OAuth completion redirect. Existing required variables still include the Google client credentials, redirect URI, Redis URL, and Fernet token encryption key.

All routes below except the Google callback require the user's Bearer access token:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/integrator/catalog` | List supported apps and current connection/enabled state. |
| `GET` | `/integrator/google/connect/{integration_key}` | Return an OAuth URL; redirect the browser to `authorization_url`. Keys: `google_sheets`, `google_drive`, `google_docs`. |
| `GET` | `/integrator/google/callback` | Google callback; redirects to `FRONTEND_URL` with `integration_status` and `integration` query parameters. |
| `PUT` | `/integrator/{integration_key}/enabled` | Enable or disable a connected app with `{"enabled": true}`. |
| `DELETE` | `/integrator/{integration_key}` | Mark only that app disconnected; keeps the shared Google grant for other apps. |

The app-specific `GET /integrator/google/{sheets,drive,docs}/connect` aliases remain available and return both `url` and `authorization_url` for compatibility.

The Google Sheets app requests the Sheets read/write scope because the registered agent tools include write operations, plus Drive metadata read-only access for spreadsheet discovery. Existing users may need to reconnect to grant the added scope. Drive and Docs currently request read-only scopes. Access tokens and refresh tokens are encrypted at rest; access tokens refresh through `GoogleCredentialFactory` and the updated expiry is persisted.

The agent exposes Drive metadata tools `search_drive_files`, `list_drive_files`, `list_drive_folder_files`, and `get_drive_file`. They can find files/folders and return metadata and open-in-Drive links. Reading file contents or editing Drive files requires expanding the Drive OAuth scope first.
