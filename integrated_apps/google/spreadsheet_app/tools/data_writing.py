from typing import Literal

from pydantic import BaseModel, Field


class WriteRange(BaseModel):
    """Arguments for writing values to a spreadsheet range."""

    spreadsheet_id: str
    range_name: str = Field(description="Target range, e.g. Sheet1!A1:C3.")
    values: list[list[str | int | float | bool | None]] = Field(
        min_length=1,
        description="Two-dimensional array of values to write."
    )
    value_input_option: Literal["RAW", "USER_ENTERED"] = "USER_ENTERED"


def write_range(
    service,
    spreadsheet_id: str,
    range_name: str,
    values: list[list[str | int | float | bool | None]],
    value_input_option: Literal["RAW", "USER_ENTERED"] = "USER_ENTERED",
):
    """Write values to a specified spreadsheet range."""
    return service.write_range(
        spreadsheet_id=spreadsheet_id,
        range_name=range_name,
        values=values,
        value_input_option=value_input_option,
    )


class UpdateCell(BaseModel):
    """Arguments for updating a single cell."""

    spreadsheet_id: str
    cell_address: str = Field(description="Cell address, e.g. Sheet1!B4.")
    value: str | int | float | bool | None
    value_input_option: Literal["RAW", "USER_ENTERED"] = "USER_ENTERED"


def update_cell(
    service,
    spreadsheet_id: str,
    cell_address: str,
    value: str | int | float | bool | None,
    value_input_option: Literal["RAW", "USER_ENTERED"] = "USER_ENTERED",
):
    """Update the value of a single spreadsheet cell."""
    return service.update_cell(
        spreadsheet_id=spreadsheet_id,
        cell_address=cell_address,
        value=value,
        value_input_option=value_input_option,
    )


class AppendRows(BaseModel):
    """Arguments for appending rows to a spreadsheet."""

    spreadsheet_id: str
    range_name: str = Field(
        description="Range used to identify the table, e.g. Sheet1!A:C."
    )
    values: list[list[str | int | float | bool | None]] = Field(
        min_length=1,
        description="Rows to append to the table."
    )
    value_input_option: Literal["RAW", "USER_ENTERED"] = "USER_ENTERED"


def append_rows(
    service,
    spreadsheet_id: str,
    range_name: str,
    values: list[list[str | int | float | bool | None]],
    value_input_option: Literal["RAW", "USER_ENTERED"] = "USER_ENTERED",
):
    """Append rows after the existing table data."""
    return service.append_rows(
        spreadsheet_id=spreadsheet_id,
        range_name=range_name,
        values=values,
        value_input_option=value_input_option,
    )


class ClearRange(BaseModel):
    """Arguments for clearing values from a spreadsheet range."""

    spreadsheet_id: str
    range_name: str = Field(description="Range to clear, e.g. Sheet1!A2:D10.")


def clear_range(
    service,
    spreadsheet_id: str,
    range_name: str,
):
    """Clear cell values while preserving formatting."""
    return service.clear_range(
        spreadsheet_id=spreadsheet_id,
        range_name=range_name,
    )
