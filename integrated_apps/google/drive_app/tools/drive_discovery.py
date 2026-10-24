from pydantic import BaseModel, Field


class SearchDriveFiles(BaseModel):
    """Arguments for searching Drive file and folder names."""

    query: str = Field(min_length=1, description="Text to find in Drive file or folder names.")
    page_size: int = Field(default=20, ge=1, le=100, description="Maximum number of matches to return.")
    page_token: str | None = Field(default=None, description="Page token from a previous search response.")


def search_drive_files(
    service,
    query: str,
    page_size: int = 20,
    page_token: str | None = None,
):
    # Pass validated tool arguments to the per-user Drive service.
    return service.list_files(query=query, page_size=page_size, page_token=page_token)


class ListDriveFiles(BaseModel):
    """Arguments for listing files visible in the connected Drive account."""

    page_size: int = Field(default=20, ge=1, le=100, description="Maximum number of files to return.")
    page_token: str | None = Field(default=None, description="Page token from a previous list response.")
    order_by: str = Field(
        default="modifiedTime desc",
        pattern=r"^(modifiedTime desc|modifiedTime|name|name desc|createdTime desc)$",
        description="Sort order for Drive results.",
    )


def list_drive_files(
    service,
    page_size: int = 20,
    page_token: str | None = None,
    order_by: str = "modifiedTime desc",
):
    # Listing defaults to recently modified files and supports pagination.
    return service.list_files(
        page_size=page_size,
        page_token=page_token,
        order_by=order_by,
    )


class ListDriveFolderFiles(BaseModel):
    """Arguments for listing files inside a Drive folder."""

    folder_id: str = Field(min_length=1, description="ID of the Drive folder to list.")
    page_size: int = Field(default=20, ge=1, le=100, description="Maximum number of files to return.")
    page_token: str | None = Field(default=None, description="Page token from a previous folder listing.")


def list_drive_folder_files(
    service,
    folder_id: str,
    page_size: int = 20,
    page_token: str | None = None,
):
    # Parent filtering is handled by Drive's query syntax and excludes trashed files.
    return service.list_files(
        folder_id=folder_id,
        page_size=page_size,
        page_token=page_token,
    )
