from integrated_apps.google.spreadsheet_app.spreadsheet_registry import tools_registry as spreadsheet_tools

def build_registry():
    registry={}

    #Register tools from google sheet
    for name, tool in  spreadsheet_tools.items():
        if name in registry:
            raise ValueError(f'Duplicate tool name:{name}')

        registry[name]=tool
    return registry

tools_registry=build_registry()