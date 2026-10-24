# sheet_client
from googleapiclient.discovery import build

def get_sheet_client(credentials):
    return build(
        'sheets',
        'v4',
        credentials=credentials
    )