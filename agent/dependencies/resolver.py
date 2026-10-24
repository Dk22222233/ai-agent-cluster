# from app.integrations.google.credentials import GoogleCredentialFactory
# from integrated_apps.google.spreadsheet_app.spreadsheet_service import (
#     SpreadsheetService,
# )
from integrated_apps.google.spreadsheet_app.provider import build_spreadsheet_service
from integrated_apps.google.drive_app.provider import build_drive_service


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
            # Registry names choose a concrete provider (for example, "drive_service").
            # Handlers deliberately use one generic `service` argument, so they stay focused on
            # their tool contract rather than knowing which provider-registration name was used.
            if "service" in resolved:
                raise ValueError("A tool may declare only one injected service")
            resolved["service"] = provider(ctx)

        return resolved


dependency_resolver = DependencyResolver(
    providers={
        "spreadsheet_service": build_spreadsheet_service,
        # Tool dependency names select the matching per-app service at dispatch time.
        "drive_service": build_drive_service,
    }
)
