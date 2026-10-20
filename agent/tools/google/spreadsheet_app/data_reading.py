
from uuid import UUID
from typing import Any

from pydantic import BaseModel, Field


# ---------- Read Range ----------

class ReadRange(BaseModel):
    """Arguments for reading a spreadsheet range."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet to read."
    )
    range_name: str = Field(
        description="A1 notation range, e.g. Sales!A1:D20."
    )
    value_render_option: str = Field(
        default="FORMATTED_VALUE",
        description=(
            "How values should be returned: "
            "FORMATTED_VALUE, UNFORMATTED_VALUE, or FORMULA."
        ),
    )


def read_range(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    range_name: str,
    value_render_option: str = "FORMATTED_VALUE",
):
    """
    Read cell values from a specified spreadsheet range.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the target spreadsheet.
        range_name: A1 notation range to read.
        value_render_option: Controls how cell values are represented.

    Returns:
        Range information and a two-dimensional array of cell values.
    """
    return service.read_range(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        range_name=range_name,
        value_render_option=value_render_option,
    )


# ---------- Read Multiple Ranges ----------

class ReadMultipleRanges(BaseModel):
    """Arguments for reading multiple spreadsheet ranges."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet to read."
    )
    ranges: list[str] = Field(
        min_length=1,
        max_length=50,
        description=(
            "A1 notation ranges, e.g. "
            "['Sales!A1:B10', 'Expenses!A1:C10']."
        ),
    )
    value_render_option: str = Field(
        default="FORMATTED_VALUE",
        description="How cell values should be represented.",
    )


def read_multiple_ranges(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    ranges: list[str],
    value_render_option: str = "FORMATTED_VALUE",
):
    """
    Read several ranges from a spreadsheet in one operation.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the target spreadsheet.
        ranges: List of A1 notation ranges.
        value_render_option: Controls how cell values are represented.

    Returns:
        Results for each requested range.
    """
    return service.read_multiple_ranges(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        ranges=ranges,
        value_render_option=value_render_option,
    )


# ---------- Get Used Range ----------

class GetUsedRange(BaseModel):
    """Arguments for finding a sheet's populated range."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet."
    )
    sheet_name: str = Field(
        description="Exact title of the sheet tab."
    )


def get_used_range(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    sheet_name: str,
):
    """
    Determine the populated range of a sheet.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the target spreadsheet.
        sheet_name: Name of the sheet tab.

    Returns:
        The detected populated range in A1 notation.
    """
    return service.get_used_range(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
    )


# ---------- Get Header Row ----------

class GetHeaderRow(BaseModel):
    """Arguments for reading column headers."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet."
    )
    sheet_name: str = Field(
        description="Exact title of the sheet tab."
    )
    header_row: int = Field(
        default=1,
        ge=1,
        description="One-based row number containing the headers.",
    )


def get_header_row(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    sheet_name: str,
    header_row: int = 1,
):
    """
    Read the column headers from a specified row.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the target spreadsheet.
        sheet_name: Name of the sheet tab.
        header_row: One-based row containing the headers.

    Returns:
        A list of header values.
    """
    return service.get_header_row(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        sheet_name=sheet_name,
        header_row=header_row,
    )


# ---------- Get Cell ----------

class GetCell(BaseModel):
    """Arguments for reading one cell."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet."
    )
    cell_address: str = Field(
        description="Cell address in A1 notation, e.g. Sales!B12."
    )


def get_cell(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    cell_address: str,
):
    """
    Read the value of a single cell.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the target spreadsheet.
        cell_address: A1 notation address of the cell.

    Returns:
        The cell value.
    """
    return service.get_cell(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        cell_address=cell_address,
    )


# ---------- Get Formulas ----------

class GetFormulas(BaseModel):
    """Arguments for reading formulas from a range."""

    spreadsheet_id: str = Field(
        description="ID of the spreadsheet."
    )
    range_name: str = Field(
        description="A1 notation range, e.g. Sales!A1:D20."
    )


def get_formulas(
    service,
    user_id: UUID,
    spreadsheet_id: str,
    range_name: str,
):
    """
    Read formulas from a range instead of calculated display values.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        spreadsheet_id: ID of the target spreadsheet.
        range_name: A1 notation range to inspect.

    Returns:
        The requested range and its formula values.
    """
    return service.get_formulas(
        user_id=user_id,
        spreadsheet_id=spreadsheet_id,
        range_name=range_name,
    )
