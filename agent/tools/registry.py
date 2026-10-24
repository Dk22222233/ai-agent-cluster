from integrated_apps.google.spreadsheet_app.spreadsheet_registry import tools_registry as spreadsheet_tools
from integrated_apps.google.drive_app.drive_registry import tools_registry as drive_tools

def build_registry():
    registry={}

    #Register tools from google sheet
    for name, tool in  spreadsheet_tools.items():
        if name in registry:
            raise ValueError(f'Duplicate tool name:{name}')
        # establish key:value pairs,
        registry[name]=tool
    # Combine Drive's tools with Sheets so the agent publishes one unified tool list.
    for name, tool in drive_tools.items():
        if name in registry:
            raise ValueError(f"Duplicate tool name:{name}")
        registry[name] = tool
    return registry

tools_registry=build_registry()
