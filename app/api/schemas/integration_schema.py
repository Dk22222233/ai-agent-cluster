from datetime import datetime

from pydantic import BaseModel


class OAuthResponse(BaseModel):
    authorization_url: str


class IntegrationStatus(BaseModel):
    # Expose connection metadata to the frontend without ever returning OAuth tokens.
    key: str
    provider: str
    name: str
    scopes: list[str]
    connected: bool
    enabled: bool
    status: str
    granted_scopes: list[str]
    last_connected_at: datetime | None = None
    provider_connected: bool


class IntegrationEnabledRequest(BaseModel):
    enabled: bool


class IntegrationActionResponse(BaseModel):
    key: str
    enabled: bool
    status: str
