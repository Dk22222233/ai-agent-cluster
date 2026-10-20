
from uuid import UUID
from typing import Any

from pydantic import BaseModel, Field


# ---------- Find Values ----------

class FindValues(BaseModel):
    """Arguments for searching cell values in a spreadsheet."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet to search."
    )

    sheet_name: str = Field(
        description="Name of the sheet tab to search."
    )

    search_text: str = Field(
        description="Text or value to find in the spreadsheet."
    )

    range_name: str | None = Field(
        default=None,
        description="Optional A1 range to limit the search, e.g. A1:D100."
    )

    match_case: bool = Field(
        default=False,
        description="Whether the search must match uppercase and lowercase letters."
    )

    match_entire_cell: bool = Field(
        default=False,
        description="Whether the entire cell must match the search text."
    )


def find_values(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    sheet_name: str,
    search_text: str,
    range_name: str | None = None,
    match_case: bool = False,
    match_entire_cell: bool = False,
) -> list[dict[str, Any]]:
    """
    Find matching cell values within a sheet or specified range.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the spreadsheet to search.
        sheet_name: Name of the sheet tab.
        search_text: Text or value to find.
        range_name: Optional range limiting the search.
        match_case: Whether capitalization must match.
        match_entire_cell: Whether the entire cell must match.

    Returns:
        A list of matches containing cell addresses and their values.
    """
    return service.find_values(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        search_text=search_text,
        range_name=range_name,
        match_case=match_case,
        match_entire_cell=match_entire_cell,
    )


# ---------- Find Rows ----------

class FindRows(BaseModel):
    """Arguments for finding rows by column value."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet to search."
    )

    sheet_name: str = Field(
        description="Name of the sheet tab to search."
    )

    column_name: str = Field(
        description="Header name of the column to search, e.g. Customer."
    )

    search_value: str = Field(
        description="Value to find in the specified column."
    )

    header_row: int = Field(
        default=1,
        ge=1,
        description="Row number containing the column headers."
    )

    match_case: bool = Field(
        default=False,
        description="Whether capitalization must match."
    )

    match_entire_cell: bool = Field(
        default=True,
        description="Whether the entire cell value must match."
    )


def find_rows(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    sheet_name: str,
    column_name: str,
    search_value: str,
    header_row: int = 1,
    match_case: bool = False,
    match_entire_cell: bool = True,
) -> list[dict[str, Any]]:
    """
    Find rows where a specified column matches a given value.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the spreadsheet to search.
        sheet_name: Name of the sheet tab.
        column_name: Header identifying the column to search.
        search_value: Value to find in that column.
        header_row: Row containing column headers.
        match_case: Whether capitalization must match.
        match_entire_cell: Whether the whole cell must match.

    Returns:
        Matching rows, including their row numbers and cell values.
    """
    return service.find_rows(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        column_name=column_name,
        search_value=search_value,
        header_row=header_row,
        match_case=match_case,
        match_entire_cell=match_entire_cell,
    )
