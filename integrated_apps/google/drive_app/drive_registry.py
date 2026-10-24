import inspect

from agent.models.llm_request_model import RegisteredTool, ToolDefinition
from integrated_apps.google.drive_app.tools.drive_discovery import (
    ListDriveFiles,
    ListDriveFolderFiles,
    SearchDriveFiles,
    list_drive_files,
    list_drive_folder_files,
    search_drive_files,
)
from integrated_apps.google.drive_app.tools.drive_metadata import GetDriveFile, get_drive_file


def register_tool(name, schema, handler):
    # Convert each Pydantic argument model into the function schema sent to the LLM.
    return RegisteredTool(
        definition=ToolDefinition(
            name=name,
            description=inspect.getdoc(schema) or "",
            parameters=schema.model_json_schema(),
        ),
        args_schema=schema,
        handler=handler,
        dependencies=("drive_service",),
    )


# Keep Drive names prefixed to avoid collisions with the existing Sheets tool registry.
tools_registry: dict[str, RegisteredTool] = {
    "search_drive_files": register_tool("search_drive_files", SearchDriveFiles, search_drive_files),
    "list_drive_files": register_tool("list_drive_files", ListDriveFiles, list_drive_files),
    "list_drive_folder_files": register_tool(
        "list_drive_folder_files", ListDriveFolderFiles, list_drive_folder_files
    ),
    "get_drive_file": register_tool("get_drive_file", GetDriveFile, get_drive_file),
}
