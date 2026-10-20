from uuid import UUID

from pydantic import BaseModel, Field


class CreateSheet(BaseModel):
    """Arguments for creating a new sheet tab."""

    spreadsheet_id: str
    title: str = Field(
        min_length=1,
        description="Name of the new sheet tab."
    )


def create_sheet(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    title: str,
):
    """Create a new sheet tab in a spreadsheet."""
    return service.create_sheet(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        title=title,
    )


class RenameSheet(BaseModel):
    """Arguments for renaming a sheet tab."""

    spreadsheet_id: str
    sheet_id: int = Field(ge=0)
    new_title: str = Field(
        min_length=1,
        description="New name for the sheet tab."
    )


def rename_sheet(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    sheet_id: int,
    new_title: str,
):
    """Rename an existing sheet tab."""
    return service.rename_sheet(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        new_title=new_title,
    )


class CopySheet(BaseModel):
    """Arguments for copying a sheet tab."""

    spreadsheet_id: str
    sheet_id: int = Field(
        ge=0,
        description="ID of the sheet to copy."
    )
    new_title: str | None = Field(
        default=None,
        description="Optional title for the copied sheet."
    )


def copy_sheet(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    sheet_id: int,
    new_title: str | None = None,
):
    """Create a copy of an existing sheet tab."""
    return service.copy_sheet(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        new_title=new_title,
    )


class DeleteSheet(BaseModel):
    """Arguments for deleting a sheet tab."""

    spreadsheet_id: str
    sheet_id: int = Field(
        ge=0,
        description="ID of the sheet tab to delete."
    )


def delete_sheet(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    sheet_id: int,
):
    """Delete a sheet tab from a spreadsheet."""
    return service.delete_sheet(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
    )