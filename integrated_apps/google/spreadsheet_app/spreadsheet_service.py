import re
from typing import Any
from uuid import UUID

from googleapiclient.discovery import build

from app.integrations.google.credentials import GoogleCredentialFactory
from integrated_apps.google.spreadsheet_app.sheet_client import get_sheet_client


class SpreadsheetService:
    def __init__(self, credential_factory: GoogleCredentialFactory, user_id: UUID):
        # Bind the authenticated user once so tool arguments never carry identity data.
        self.credential_factory = credential_factory
        self.user_id = user_id

    def _credentials(self):
        return self.credential_factory.get_credentials(self.user_id)

    def build_client(self):
        # Every Sheets API call uses credentials for the user bound by the request provider.
        return get_sheet_client(self._credentials())

    def _drive_client(self):
        # Drive metadata is needed to find spreadsheets because the Sheets API has no file search endpoint.
        return build("drive", "v3", credentials=self._credentials())

    @staticmethod
    def _quote_sheet(sheet_name: str) -> str:
        return "'" + sheet_name.replace("'", "''") + "'"

    @staticmethod
    def _column_index(column: str) -> int:
        result = 0
        for character in column.upper():
            result = result * 26 + ord(character) - ord("A") + 1
        return result - 1

    @staticmethod
    def _column_label(index: int) -> str:
        label = ""
        while index >= 0:
            index, remainder = divmod(index, 26)
            label = chr(remainder + ord("A")) + label
            index -= 1
        return label

    @classmethod
    def _parse_range(cls, range_name: str) -> tuple[str, int, int, int, int]:
        # Parse a bounded A1 range for grid-based sort requests and match coordinates.
        match = re.fullmatch(r"'?(.+?)'?!\$?([A-Z]+)\$?(\d+):\$?([A-Z]+)\$?(\d+)", range_name, re.I)
        if not match:
            raise ValueError("Expected a bounded A1 range such as Sales!A1:D20")
        sheet, start_col, start_row, end_col, end_row = match.groups()
        return sheet.replace("''", "'"), int(start_row), cls._column_index(start_col), int(end_row), cls._column_index(end_col)

    @staticmethod
    def _numeric_or_text(value: Any):
        if isinstance(value, bool):
            return (0, str(value).casefold())
        if isinstance(value, (int, float)):
            return (0, value)
        try:
            return (0, float(str(value).replace(",", "")))
        except (ValueError, TypeError):
            return (1, str(value).casefold())

    def search_spreadsheets(self, query: str, page_size: int = 10) -> dict:
        escaped = query.replace("\\", "\\\\").replace("'", "\\'")
        response = self._drive_client().files().list(
            q=f"mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false and name contains '{escaped}'",
            pageSize=page_size,
            orderBy="modifiedTime desc",
            fields="nextPageToken,files(id,name,mimeType,modifiedTime,webViewLink)",
        ).execute()
        return {"spreadsheets": response.get("files", []), "next_page_token": response.get("nextPageToken")}

    def list_spreadsheets(self, page_size: int = 20, page_token: str | None = None) -> dict:
        response = self._drive_client().files().list(
            q="mimeType = 'application/vnd.google-apps.spreadsheet' and trashed = false",
            pageSize=page_size,
            pageToken=page_token,
            orderBy="modifiedTime desc",
            fields="nextPageToken,files(id,name,mimeType,modifiedTime,webViewLink)",
        ).execute()
        return {"spreadsheets": response.get("files", []), "next_page_token": response.get("nextPageToken")}

    def get_spreadsheet(self, spreadsheet_id: str) -> dict:
        return self.build_client().spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="spreadsheetId,spreadsheetUrl,properties,sheets(properties)",
        ).execute()

    def list_sheets(self, spreadsheet_id: str) -> list[dict]:
        spreadsheet = self.get_spreadsheet(spreadsheet_id)
        return [sheet.get("properties", {}) for sheet in spreadsheet.get("sheets", [])]

    def get_sheet(self, spreadsheet_id: str, sheet_name: str | None = None, sheet_id: int | None = None) -> dict:
        sheets = self.list_sheets(spreadsheet_id)
        for sheet in sheets:
            if (sheet_name is not None and sheet.get("title") == sheet_name) or (
                sheet_id is not None and sheet.get("sheetId") == sheet_id
            ):
                return sheet
        raise ValueError("Sheet tab not found")

    def get_spreadsheet_url(self, spreadsheet_id: str) -> str:
        return self.get_spreadsheet(spreadsheet_id).get(
            "spreadsheetUrl", f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
        )

    def read_range(self, spreadsheet_id: str, range_name: str, value_render_option: str = "FORMATTED_VALUE") -> dict:
        return self.build_client().spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueRenderOption=value_render_option,
        ).execute()

    def read_multiple_ranges(self, spreadsheet_id: str, ranges: list[str], value_render_option: str = "FORMATTED_VALUE") -> dict:
        return self.build_client().spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id,
            ranges=ranges,
            valueRenderOption=value_render_option,
        ).execute()

    def get_used_range(self, spreadsheet_id: str, sheet_name: str) -> str:
        sheet = self.get_sheet(spreadsheet_id, sheet_name=sheet_name)
        grid = sheet.get("gridProperties", {})
        row_limit = min(grid.get("rowCount", 1000), 10000)
        column_limit = min(grid.get("columnCount", 26), 702)
        end_column = self._column_label(max(column_limit - 1, 0))
        quoted = self._quote_sheet(sheet_name)
        values = self.read_range(spreadsheet_id, f"{quoted}!A1:{end_column}{row_limit}").get("values", [])
        last_row = max((index for index, row in enumerate(values, 1) if any(value != "" for value in row)), default=0)
        last_column = max((col for row in values for col, value in enumerate(row, 1) if value != ""), default=0)
        if last_row == 0 or last_column == 0:
            return f"{quoted}!A1"
        return f"{quoted}!A1:{self._column_label(last_column - 1)}{last_row}"

    def get_header_row(self, spreadsheet_id: str, sheet_name: str, header_row: int = 1) -> list:
        quoted = self._quote_sheet(sheet_name)
        result = self.read_range(spreadsheet_id, f"{quoted}!{header_row}:{header_row}")
        return (result.get("values") or [[]])[0]

    def get_cell(self, spreadsheet_id: str, cell_address: str) -> dict:
        return self.read_range(spreadsheet_id, cell_address)

    def get_formulas(self, spreadsheet_id: str, range_name: str) -> dict:
        return self.read_range(spreadsheet_id, range_name, value_render_option="FORMULA")

    def find_values(
        self, spreadsheet_id: str, sheet_name: str, search_text: str, range_name: str | None = None,
        match_case: bool = False, match_entire_cell: bool = False,
    ) -> list[dict]:
        target_range = range_name or f"{self._quote_sheet(sheet_name)}!A:ZZ"
        start_row, start_col = 1, 0
        try:
            _, start_row, start_col, _, _ = self._parse_range(target_range)
        except ValueError:
            # A tool may provide an unqualified range such as B5:D20 within sheet_name.
            unqualified = re.fullmatch(r"\$?([A-Z]+)\$?(\d+):\$?([A-Z]+)\$?(\d+)", target_range, re.I)
            if unqualified:
                start_col = self._column_index(unqualified.group(1))
                start_row = int(unqualified.group(2))
        values = self.read_range(spreadsheet_id, target_range).get("values", [])
        target = search_text if match_case else search_text.casefold()
        matches = []
        for row_index, row in enumerate(values):
            for col_index, value in enumerate(row):
                cell_value = str(value)
                candidate = cell_value if match_case else cell_value.casefold()
                matched = candidate == target if match_entire_cell else target in candidate
                if matched:
                    matches.append({
                        "cell": f"{self._column_label(start_col + col_index)}{start_row + row_index}",
                        "value": value,
                    })
        return matches

    def find_rows(
        self, spreadsheet_id: str, sheet_name: str, column_name: str, search_value: str,
        header_row: int = 1, match_case: bool = False, match_entire_cell: bool = True,
    ) -> list[dict]:
        used_range = self.get_used_range(spreadsheet_id, sheet_name)
        rows = self.read_range(spreadsheet_id, used_range).get("values", [])
        header_index = header_row - 1
        if header_index >= len(rows):
            return []
        headers = rows[header_index]
        try:
            column_index = headers.index(column_name)
        except ValueError as exc:
            raise ValueError(f"Column header not found: {column_name}") from exc
        target = search_value if match_case else search_value.casefold()
        matches = []
        for row_number, row in enumerate(rows[header_index + 1:], header_row + 1):
            value = row[column_index] if column_index < len(row) else ""
            candidate = str(value) if match_case else str(value).casefold()
            matched = candidate == target if match_entire_cell else target in candidate
            if matched:
                matches.append({"row_number": row_number, "values": row})
        return matches

    def sort_range(
        self, spreadsheet_id: str, range_name: str, sort_by_column: str,
        ascending: bool = True, has_header: bool = True,
    ) -> dict:
        sheet_name, start_row, start_col, end_row, end_col = self._parse_range(range_name)
        sheet = self.get_sheet(spreadsheet_id, sheet_name=sheet_name)
        values = self.read_range(spreadsheet_id, range_name).get("values", [])
        headers = values[0] if has_header and values else []
        if has_header:
            try:
                sort_index = headers.index(sort_by_column)
            except ValueError as exc:
                raise ValueError(f"Sort column not found: {sort_by_column}") from exc
            sort_index += start_col
            sort_start = start_row - 1
        else:
            sort_index = (
                self._column_index(sort_by_column)
                if sort_by_column.isalpha()
                else start_col + int(sort_by_column) - 1
            )
            sort_start = start_row - 1
        request = {
            "sortRange": {
                "range": {
                    "sheetId": sheet["sheetId"],
                    "startRowIndex": sort_start + (1 if has_header else 0),
                    "endRowIndex": end_row,
                    "startColumnIndex": start_col,
                    "endColumnIndex": end_col + 1,
                },
                "sortSpecs": [{"dimensionIndex": sort_index, "sortOrder": "ASCENDING" if ascending else "DESCENDING"}],
            }
        }
        return self.build_client().spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body={"requests": [request]}
        ).execute()

    def filter_rows(
        self, spreadsheet_id: str, sheet_name: str, column_name: str, operator: str,
        value: str, header_row: int = 1, limit: int = 100,
    ) -> list[dict]:
        rows = self.read_range(spreadsheet_id, self.get_used_range(spreadsheet_id, sheet_name)).get("values", [])
        header_index = header_row - 1
        if header_index >= len(rows):
            return []
        headers = rows[header_index]
        try:
            column_index = headers.index(column_name)
        except ValueError as exc:
            raise ValueError(f"Column header not found: {column_name}") from exc
        matches = []
        target = self._numeric_or_text(value)
        for row_number, row in enumerate(rows[header_index + 1:], header_row + 1):
            cell = row[column_index] if column_index < len(row) else ""
            cell_text = str(cell).casefold()
            target_text = str(value).casefold()
            left, right = self._numeric_or_text(cell), target
            checks = {
                "equals": cell_text == target_text,
                "not_equals": cell_text != target_text,
                "contains": target_text in cell_text,
                "greater_than": left > right,
                "less_than": left < right,
                "greater_or_equal": left >= right,
                "less_or_equal": left <= right,
            }
            if operator not in checks:
                raise ValueError(f"Unsupported filter operator: {operator}")
            if checks[operator]:
                matches.append({"row_number": row_number, "values": row})
                if len(matches) >= limit:
                    break
        return matches

    def summarize_column(self, spreadsheet_id: str, sheet_name: str, column_name: str, header_row: int = 1) -> dict:
        rows = self.read_range(spreadsheet_id, self.get_used_range(spreadsheet_id, sheet_name)).get("values", [])
        header_index = header_row - 1
        if header_index >= len(rows):
            raise ValueError("Header row not found")
        try:
            column_index = rows[header_index].index(column_name)
        except ValueError as exc:
            raise ValueError(f"Column header not found: {column_name}") from exc
        numbers = []
        for row in rows[header_index + 1:]:
            try:
                numbers.append(float(str(row[column_index]).replace(",", "")))
            except (ValueError, IndexError):
                continue
        return {
            "column": column_name,
            "count": len(numbers),
            "sum": sum(numbers),
            "average": sum(numbers) / len(numbers) if numbers else None,
            "minimum": min(numbers) if numbers else None,
            "maximum": max(numbers) if numbers else None,
        }

    def write_range(self, spreadsheet_id: str, range_name: str, values: list[list], value_input_option: str = "USER_ENTERED") -> dict:
        return self.build_client().spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name, valueInputOption=value_input_option,
            body={"values": values},
        ).execute()

    def update_cell(self, spreadsheet_id: str, cell_address: str, value: Any, value_input_option: str = "USER_ENTERED") -> dict:
        return self.write_range(spreadsheet_id, cell_address, [[value]], value_input_option)

    def append_rows(self, spreadsheet_id: str, range_name: str, values: list[list], value_input_option: str = "USER_ENTERED") -> dict:
        return self.build_client().spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name, valueInputOption=value_input_option,
            insertDataOption="INSERT_ROWS", body={"values": values},
        ).execute()

    def clear_range(self, spreadsheet_id: str, range_name: str) -> dict:
        return self.build_client().spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range=range_name, body={},
        ).execute()

    def create_sheet(self, spreadsheet_id: str, title: str) -> dict:
        return self.build_client().spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": [{"addSheet": {"properties": {"title": title}}}]},
        ).execute()

    def rename_sheet(self, spreadsheet_id: str, sheet_id: int, new_title: str) -> dict:
        return self.build_client().spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": [{"updateSheetProperties": {
                "properties": {"sheetId": sheet_id, "title": new_title}, "fields": "title"
            }}]},
        ).execute()

    def copy_sheet(self, spreadsheet_id: str, sheet_id: int, new_title: str | None = None) -> dict:
        result = self.build_client().spreadsheets().sheets().copyTo(
            spreadsheetId=spreadsheet_id, sheetId=sheet_id, body={"destinationSpreadsheetId": spreadsheet_id},
        ).execute()
        if new_title:
            self.rename_sheet(spreadsheet_id, result["sheetId"], new_title)
            result["title"] = new_title
        return result

    def delete_sheet(self, spreadsheet_id: str, sheet_id: int) -> dict:
        return self.build_client().spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": [{"deleteSheet": {"sheetId": sheet_id}}]},
        ).execute()
