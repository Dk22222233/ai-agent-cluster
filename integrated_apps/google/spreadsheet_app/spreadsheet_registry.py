
# agent/tools/google/spreadsheet_app/registry.py

from agent.models.llm_request_model import ToolDefinition, RegisteredTool

from integrated_apps.google.spreadsheet_app.tools.spreadsheet_discovery import (
    search_spreadsheets,
    SearchSpreadsheets,
    list_spreadsheets,
    ListSpreadsheets,
)

from integrated_apps.google.spreadsheet_app.tools.spreadsheet_metadata import (
    get_spreadsheet,
    GetSpreadsheet,
    list_sheets,
    ListSheets,
    get_sheet,
    GetSheet,
    get_spreadsheet_url,
    GetSpreadsheetUrl,
)

from integrated_apps.google.spreadsheet_app.tools.data_reading import (
    read_range,
    ReadRange,
    read_multiple_ranges,
    ReadMultipleRanges,
    get_used_range,
    GetUsedRange,
    get_header_row,
    GetHeaderRow,
    get_cell,
    GetCell,
    get_formulas,
    GetFormulas,
)

from integrated_apps.google.spreadsheet_app.tools.data_search import (
    find_values,
    FindValues,
    find_rows,
    FindRows,
)

from integrated_apps.google.spreadsheet_app.tools.data_analysis import (
    sort_range,
    SortRange,
    filter_rows,
    FilterRows,
    summarize_column,
    SummarizeColumn,
)

from integrated_apps.google.spreadsheet_app.tools.data_writing import (
    write_range,
    WriteRange,
    update_cell,
    UpdateCell,
    append_rows,
    AppendRows,
    clear_range,
    ClearRange,
)

from integrated_apps.google.spreadsheet_app.tools.spreadsheet_management import (
    create_sheet,
    CreateSheet,
    rename_sheet,
    RenameSheet,
    copy_sheet,
    CopySheet,
    delete_sheet,
    DeleteSheet,
)
import inspect

def register_tool(name,  schema, handler):
    description=inspect.getdoc(schema) or ''
    return RegisteredTool(

        definition=ToolDefinition(
            name=name,
            description=description,
            parameters=schema.model_json_schema(),
        ),
        args_schema=schema,
        handler=handler,
        dependencies=("spreadsheet_service",),
    )


tools_registry: dict[str, RegisteredTool] = {
    # 1. Spreadsheet discovery
    "search_spreadsheets": register_tool(
        "search_spreadsheets",

        SearchSpreadsheets,
        search_spreadsheets,
    ),
    "list_spreadsheets": register_tool(
        "list_spreadsheets",

        ListSpreadsheets,
        list_spreadsheets,
    ),

    # 2. Spreadsheet metadata
    "get_spreadsheet": register_tool(
        "get_spreadsheet",

        GetSpreadsheet,
        get_spreadsheet,
    ),
    "list_sheets": register_tool(
        "list_sheets",

        ListSheets,
        list_sheets,
    ),
    "get_sheet": register_tool(
        "get_sheet",

        GetSheet,
        get_sheet,
    ),
    "get_spreadsheet_url": register_tool(
        "get_spreadsheet_url",

        GetSpreadsheetUrl,
        get_spreadsheet_url,
    ),

    # 3. Data reading
    "read_range": register_tool(
        "read_range",

        ReadRange,
        read_range,
    ),
    "read_multiple_ranges": register_tool(
        "read_multiple_ranges",
  
        ReadMultipleRanges,
        read_multiple_ranges,
    ),
    "get_used_range": register_tool(
        "get_used_range",

        GetUsedRange,
        get_used_range,
    ),
    "get_header_row": register_tool(
        "get_header_row",

        GetHeaderRow,
        get_header_row,
    ),
    "get_cell": register_tool(
        "get_cell",

        GetCell,
        get_cell,
    ),
    "get_formulas": register_tool(
        "get_formulas",
  
        GetFormulas,
        get_formulas,
    ),

    # 4. Data search
    "find_values": register_tool(
        "find_values",

        FindValues,
        find_values,
    ),
    "find_rows": register_tool(
        "find_rows",

        FindRows,
        find_rows,
    ),

    # 5. Data analysis
    "sort_range": register_tool(
        "sort_range",
   
        SortRange,
        sort_range,
    ),
    "filter_rows": register_tool(
        "filter_rows",
     
        FilterRows,
        filter_rows,
    ),
    "summarize_column": register_tool(
        "summarize_column",

        SummarizeColumn,
        summarize_column,
    ),

    # 6. Data writing
    "write_range": register_tool(
        "write_range",

        WriteRange,
        write_range,
    ),
    "update_cell": register_tool(
        "update_cell",
  
        UpdateCell,
        update_cell,
    ),
    "append_rows": register_tool(
        "append_rows",

        AppendRows,
        append_rows,
    ),
    "clear_range": register_tool(
        "clear_range",
   
        ClearRange,
        clear_range,
    ),

    # 7. Sheet management
    "create_sheet": register_tool(
        "create_sheet",

        CreateSheet,
        create_sheet,
    ),
    "rename_sheet": register_tool(
        "rename_sheet",

        RenameSheet,
        rename_sheet,
    ),
    "copy_sheet": register_tool(
        "copy_sheet",
   
        CopySheet,
        copy_sheet,
    ),
    "delete_sheet": register_tool(
        "delete_sheet",
   
        DeleteSheet,
        delete_sheet,
    ),
}
