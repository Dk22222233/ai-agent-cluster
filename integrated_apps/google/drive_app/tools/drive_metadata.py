from pydantic import BaseModel, Field


class GetDriveFile(BaseModel):
    """Arguments for retrieving metadata for one Drive file or folder."""

    file_id: str = Field(min_length=1, description="ID of the Drive file or folder to inspect.")


def get_drive_file(service, file_id: str):
    # Return metadata and a webViewLink; content access requires an additional Drive scope.
    return service.get_file(file_id=file_id)
