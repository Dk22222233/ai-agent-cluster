
from uuid import UUID
from typing import Any

from pydantic import BaseModel, Field


# ---------- Sort Range ----------

class SortRange(BaseModel):
    """Arguments for sorting spreadsheet rows."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet."
    )

    range_name: str = Field(
        description="A1 range containing the data to sort, e.g. Sales!A1:D100."
    )

    sort_by_column: str = Field(
        description=(
            "Column header to sort by, e.g. Revenue or Date."
        )
    )

    ascending: bool = Field(
        default=True,
        description="Sort in ascending order when true, descending otherwise."
    )

    has_header: bool = Field(
        default=True,
        description="Whether the first row of the range contains headers."
    )


def sort_range(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    range_name: str,
    sort_by_column: str,
    ascending: bool = True,
    has_header: bool = True,
):
    """
    Sort rows in a range using a column header.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the spreadsheet.
        range_name: A1 range containing the data.
        sort_by_column: Header of the column used for sorting.
        ascending: Whether to sort in ascending order.
        has_header: Whether the first row contains headers.

    Returns:
        Result describing the completed sort operation.
    """
    return service.sort_range(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        range_name=range_name,
        sort_by_column=sort_by_column,
        ascending=ascending,
        has_header=has_header,
    )


# ---------- Filter Rows ----------

class FilterRows(BaseModel):
    """Arguments for selecting rows that match a condition."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet."
    )

    sheet_name: str = Field(
        description="Name of the sheet containing the data."
    )

    column_name: str = Field(
        description="Column header to evaluate, e.g. Status."
    )

    operator: str = Field(
        description=(
            "Comparison operator: equals, not_equals, contains, "
            "greater_than, less_than, greater_or_equal, less_or_equal."
        )
    )

    value: str = Field(
        description="Value against which the column cells are compared."
    )

    header_row: int = Field(
        default=1,
        ge=1,
        description="Row number containing column headers."
    )

    limit: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum number of matching rows to return."
    )


def filter_rows(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    sheet_name: str,
    column_name: str,
    operator: str,
    value: str,
    header_row: int = 1,
    limit: int = 100,
):
    """
    Return rows whose specified column matches a condition.

    This operation selects matching records; it does not create or
    modify a Google Sheets filter.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the spreadsheet.
        sheet_name: Name of the sheet to inspect.
        column_name: Header of the column to evaluate.
        operator: Supported comparison operator.
        value: Comparison value.
        header_row: Row containing the column headers.
        limit: Maximum number of matching rows.

    Returns:
        Matching rows and their row numbers.
    """
    return service.filter_rows(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        column_name=column_name,
        operator=operator,
        value=value,
        header_row=header_row,
        limit=limit,
    )


# ---------- Summarize Column ----------

class SummarizeColumn(BaseModel):
    """Arguments for calculating summary statistics."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet."
    )

    sheet_name: str = Field(
        description="Name of the sheet containing the data."
    )

    column_name: str = Field(
        description="Header of the numeric column to summarize."
    )

    header_row: int = Field(
        default=1,
        ge=1,
        description="Row containing the column headers."
    )


def summarize_column(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    sheet_name: str,
    column_name: str,
    header_row: int = 1,
) -> dict[str, Any]:
    """
    Calculate summary statistics for a numeric column.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the spreadsheet.
        sheet_name: Name of the sheet to analyze.
        column_name: Header of the numeric column.
        header_row: Row containing the column headers.

    Returns:
        Summary statistics such as count, sum, average, minimum,
        and maximum, as supported by the service.
    """
    return service.summarize_column(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        column_name=column_name,
        header_row=header_row,
    )
