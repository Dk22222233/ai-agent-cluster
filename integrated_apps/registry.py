# from agent.tools.google.spreadsheet_app.spreadsheet_discovery import (
#     search_spreadsheets,
#     SearchSpreadsheets,
#     list_spreadsheets,
#     ListSpreadsheets,
# )

# from agent.tools.google.spreadsheet_app.spreadsheet_metadata import (
#     get_spreadsheet,
#     GetSpreadsheet,
#     list_sheets,
#     ListSheets,
#     get_sheet,
#     GetSheet,
#     get_spreadsheet_url,
#     GetSpreadsheetUrl,
# )

# from agent.tools.google.spreadsheet_app.data_reading import (
#     read_range,
#     ReadRange,
#     read_multiple_ranges,
#     ReadMultipleRanges,
#     get_used_range,
#     GetUsedRange,
#     get_header_row,
#     GetHeaderRow,
#     get_cell,
#     GetCell,
#     get_formulas,
#     GetFormulas,
# )

# from agent.tools.google.spreadsheet_app.data_search import (
#     find_values,
#     FindValues,
#     find_rows,
#     FindRows,
# )

# from agent.tools.google.spreadsheet_app.data_analysis import (
#     sort_range,
#     SortRange,
#     filter_rows,
#     FilterRows,
#     summarize_column,
#     SummarizeColumn,
# )

# from agent.tools.google.spreadsheet_app.data_writing import (
#     write_range,
#     WriteRange,
#     update_cell,
#     UpdateCell,
#     append_rows,
#     AppendRows,
#     clear_range,
#     ClearRange,
# )

# from agent.tools.google.spreadsheet_app.spreadsheet_management import (
#     create_sheet,
#     CreateSheet,
#     rename_sheet,
#     RenameSheet,
#     copy_sheet,
#     CopySheet,
#     delete_sheet,
#     DeleteSheet,
# )


# tools_registry = {
#     # 1. Spreadsheet discovery
#     "search_spreadsheets": {
#         "function": search_spreadsheets,
#         "schema": SearchSpreadsheets,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "list_spreadsheets": {
#         "function": list_spreadsheets,
#         "schema": ListSpreadsheets,
#         "dependencies": ["spreadsheet_service"],
#     },

#     # 2. Spreadsheet metadata
#     "get_spreadsheet": {
#         "function": get_spreadsheet,
#         "schema": GetSpreadsheet,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "list_sheets": {
#         "function": list_sheets,
#         "schema": ListSheets,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "get_sheet": {
#         "function": get_sheet,
#         "schema": GetSheet,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "get_spreadsheet_url": {
#         "function": get_spreadsheet_url,
#         "schema": GetSpreadsheetUrl,
#         "dependencies": ["spreadsheet_service"],
#     },

#     # 3. Data reading
#     "read_range": {
#         "function": read_range,
#         "schema": ReadRange,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "read_multiple_ranges": {
#         "function": read_multiple_ranges,
#         "schema": ReadMultipleRanges,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "get_used_range": {
#         "function": get_used_range,
#         "schema": GetUsedRange,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "get_header_row": {
#         "function": get_header_row,
#         "schema": GetHeaderRow,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "get_cell": {
#         "function": get_cell,
#         "schema": GetCell,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "get_formulas": {
#         "function": get_formulas,
#         "schema": GetFormulas,
#         "dependencies": ["spreadsheet_service"],
#     },

#     # 4. Data search
#     "find_values": {
#         "function": find_values,
#         "schema": FindValues,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "find_rows": {
#         "function": find_rows,
#         "schema": FindRows,
#         "dependencies": ["spreadsheet_service"],
#     },

#     # 5. Data analysis
#     "sort_range": {
#         "function": sort_range,
#         "schema": SortRange,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "filter_rows": {
#         "function": filter_rows,
#         "schema": FilterRows,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "summarize_column": {
#         "function": summarize_column,
#         "schema": SummarizeColumn,
#         "dependencies": ["spreadsheet_service"],
#     },

#     # 6. Data writing
#     "write_range": {
#         "function": write_range,
#         "schema": WriteRange,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "update_cell": {
#         "function": update_cell,
#         "schema": UpdateCell,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "append_rows": {
#         "function": append_rows,
#         "schema": AppendRows,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "clear_range": {
#         "function": clear_range,
#         "schema": ClearRange,
#         "dependencies": ["spreadsheet_service"],
#     },

#     # 7. Sheet management
#     "create_sheet": {
#         "function": create_sheet,
#         "schema": CreateSheet,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "rename_sheet": {
#         "function": rename_sheet,
#         "schema": RenameSheet,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "copy_sheet": {
#         "function": copy_sheet,
#         "schema": CopySheet,
#         "dependencies": ["spreadsheet_service"],
#     },
#     "delete_sheet": {
#         "function": delete_sheet,
#         "schema": DeleteSheet,
#         "dependencies": ["spreadsheet_service"],
#     },
# }