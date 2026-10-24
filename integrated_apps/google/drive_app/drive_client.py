from googleapiclient.discovery import build


def get_drive_client(credentials):
    # Build the official Drive v3 client using the user's refreshed OAuth credentials.
    return build("drive", "v3", credentials=credentials)
