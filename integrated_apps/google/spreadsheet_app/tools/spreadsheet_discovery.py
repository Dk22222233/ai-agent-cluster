
from pydantic import BaseModel, Field
from uuid import UUID


# ---------- Search Spreadsheets ----------

class SearchSpreadsheets(BaseModel):
    """Arguments for searching spreadsheets."""

    query: str = Field(
        description="Spreadsheet name or keywords to search for."
    )

    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of spreadsheets to return."
    )


def search_spreadsheets(
    service,
    user_id: UUID,
    query: str,
    page_size: int = 10,
):
    """
    Search for spreadsheets accessible to the user's connected Google account.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        query: Name or keywords to search for.
        page_size: Maximum number of results.

    Returns:
        Matching spreadsheet metadata.
    """
    return service.search_spreadsheets(
        user_id=user_id,
        query=query,
        page_size=page_size,
    )


# ---------- List Spreadsheets ----------

class ListSpreadsheets(BaseModel):
    """Arguments for listing available spreadsheets."""

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of spreadsheets to return."
    )

    page_token: str | None = Field(
        default=None,
        description="Pagination token from a previous result, if available."
    )


def list_spreadsheets(
    service,
    user_id: UUID,
    page_size: int = 20,
    page_token: str | None = None,
):
    """
    List spreadsheets accessible to the user's connected Google account.

    Args:
        service: Injected spreadsheet service.
        user_id: Authenticated application user ID.
        page_size: Maximum number of results.
        page_token: Token for retrieving the next page.

    Returns:
        A page of spreadsheet metadata and, ideally, a next-page token.
    """
    return service.list_spreadsheets(
        user_id=user_id,
        page_size=page_size,
        page_token=page_token,
    )