
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


# ---------- Get Spreadsheet Metadata ----------

class GetSpreadsheet(BaseModel):
    """Arguments for retrieving spreadsheet metadata."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet to inspect."
    )


def get_spreadsheet(
    service,
    user_id: UUID,
    spreadsheet_id: str,
):
    """
    Retrieve spreadsheet metadata, including its title and URL.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the target spreadsheet.

    Returns:
        Spreadsheet metadata.
    """
    return service.get_spreadsheet(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
    )


# ---------- List Sheets ----------

class ListSheets(BaseModel):
    """Arguments for listing tabs in a spreadsheet."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet whose tabs should be listed."
    )


def list_sheets(
    service,
    user_id: UUID,
    spreadsheet_id: str,
):
    """
    List all tabs in a spreadsheet, including their IDs, titles,
    positions, and grid dimensions.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the target spreadsheet.

    Returns:
        A list of sheet metadata.
    """
    return service.list_sheets(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
    )


# ---------- Get Sheet Metadata ----------

class GetSheet(BaseModel):
    """Arguments for retrieving a specific tab's metadata."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet containing the tab."
    )

    sheet_name: str | None = Field(
        default=None,
        description="Exact title of the tab to retrieve."
    )

    sheet_id: int | None = Field(
        default=None,
        description="Numeric ID of the tab to retrieve."
    )

    @model_validator(mode="after")
    def validate_sheet_identifier(self):
        if (self.sheet_name is None) == (self.sheet_id is None):
            raise ValueError(
                "Provide exactly one of sheet_name or sheet_id."
            )
        return self


def get_sheet(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    sheet_name: str | None = None,
    sheet_id: int | None = None,
):
    """
    Retrieve metadata for one tab, identified by its name or numeric ID.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the parent spreadsheet.
        sheet_name: Exact tab title, if using its name.
        sheet_id: Numeric tab ID, if using its ID.

    Returns:
        Metadata for the requested tab.
    """
    return service.get_sheet(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        sheet_id=sheet_id,
    )


# ---------- Get Spreadsheet URL ----------

class GetSpreadsheetUrl(BaseModel):
    """Arguments for retrieving a spreadsheet URL."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet to open."
    )


def get_spreadsheet_url(
    service,
    user_id: UUID,
    spreadsheet_id: str,
):
    """
    Retrieve the URL of a spreadsheet so the user can open it.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the target spreadsheet.

    Returns:
        The spreadsheet URL.
    """
    return service.get_spreadsheet_url(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
    )
