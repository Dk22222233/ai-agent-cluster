# from app.integrations.google.credentials import GoogleCredentialFactory
# from integrated_apps.google.spreadsheet_app.spreadsheet_service import (
#     SpreadsheetService,
# )
from integrated_apps.google.spreadsheet_app.provider import build_spreadsheet_service


class DependencyResolver:
    def __init__(self, providers: dict):
        self.providers = providers

    def resolve(self, dependencies: tuple, ctx) -> dict:
        resolved = {}

        for name in dependencies:
            # --provider contains many services, the tool being selected get its dependency by the name in the registry
            provider = self.providers.get(name)

            if provider is None:
                raise ValueError(
                    f"Dependency provider not found: {name}"
                )
            #----after picking the right service for selected tool, the resolved save it in dict and provider(ctx)
            #---the context is passed
            resolved[name] = provider(ctx)

        return resolved


dependency_resolver = DependencyResolver(
    providers={
        "spreadsheet_service": build_spreadsheet_service,
    }
)
