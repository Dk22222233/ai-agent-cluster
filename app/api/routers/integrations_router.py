from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.api.schemas import (
    IntegrationActionResponse,
    IntegrationEnabledRequest,
    IntegrationStatus,
    OAuthResponse,
    UserResponse,
)
from app.services.integration_service import integration_service
from config import settings
from agent import get_logger


router = APIRouter(prefix="/integrator", tags=["Integrations"])
logger = get_logger(__name__)


# Shared helper keeps generic and app-specific OAuth URL responses consistent.
def _start_connection(integration_key: str, current_user: UserResponse) -> dict:
    try:
        authorization_url = integration_service.start_google_oauth(current_user.id, integration_key)
        return {"authorization_url": authorization_url, "url": authorization_url}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/catalog", response_model=list[IntegrationStatus])
def list_integrations(
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List supported integrated apps with this user's connection state."""
    # Return all registered apps so the frontend can render connected and unconnected states.
    return integration_service.list_user_integrations(current_user.id, db)


@router.get("/google/connect/{integration_key}", response_model=OAuthResponse)
def connect_google_app(
    integration_key: str,
    current_user: UserResponse = Depends(get_current_user),
):
    """Return an OAuth URL for any registered Google app."""
    # A single generic endpoint lets the frontend start OAuth for future registered Google apps.
    result = _start_connection(integration_key, current_user)
    return {"authorization_url": result["authorization_url"]}


@router.get("/google/sheets/connect")
def connect_sheets(current_user: UserResponse = Depends(get_current_user)):
    return _start_connection("google_sheets", current_user)


@router.get("/google/drive/connect")
def connect_drive(current_user: UserResponse = Depends(get_current_user)):
    return _start_connection("google_drive", current_user)


@router.get("/google/docs/connect")
def connect_docs(current_user: UserResponse = Depends(get_current_user)):
    return _start_connection("google_docs", current_user)


@router.put("/{integration_key}/enabled", response_model=IntegrationActionResponse)
def set_integration_enabled(
    integration_key: str,
    request: IntegrationEnabledRequest,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Enable state is scoped to this app installation, not the shared provider connection.
    try:
        return integration_service.set_enabled(current_user.id, integration_key, request.enabled, db)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{integration_key}", response_model=IntegrationActionResponse)
def disconnect_integration(
    integration_key: str,
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Disable one app installation while retaining the shared Google grant for other apps."""
    # Disconnecting one app preserves the Google grant used by any other enabled app.
    try:
        return integration_service.disconnect(current_user.id, integration_key, db)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/google/callback")
def google_callback(
    code: str | None = Query(default=None),
    state: str = Query(...),
    error: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """OAuth callback; one-time state identifies the user and app."""
    # Callback identity comes from one-time state rather than browser-supplied user IDs.
    frontend = settings.FRONTEND_URL.rstrip("/")
    if error or not code:
        reason = "denied" if error else "missing_code"
        return RedirectResponse(f"{frontend}/?integration_status=error&reason={reason}")
    try:
        result = integration_service.finish_google_oauth(code=code, state=state, db=db)
        return RedirectResponse(
            f"{frontend}/?integration_status=success&integration={result['integration_key']}"
        )
    except ValueError as exc:
        # Return a safe, actionable code to the frontend while retaining the detailed cause in server logs.
        message = str(exc).lower()
        if "oauth state" in message:
            reason = "expired_or_used_state"
        elif "refresh token" in message:
            reason = "missing_refresh_token"
        elif "granted scopes" in message:
            reason = "missing_granted_scopes"
        else:
            reason = "oauth_validation_failed"
        logger.warning("Google OAuth callback rejected: %s", exc)
        return RedirectResponse(f"{frontend}/?integration_status=error&reason={reason}")
    except Exception as exc:
        db.rollback()
        # Token-exchange and persistence failures need traceback logging, but never expose details or tokens in URLs.
        logger.exception("Google OAuth callback failed: %s", exc)
        return RedirectResponse(f"{frontend}/?integration_status=error&reason=token_exchange_or_persistence_failed")
