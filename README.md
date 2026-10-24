# Agent Cluster

An authenticated AI agent with Google Sheets and Google Drive tools. The important rule of this codebase is:

> **Routers handle HTTP, handlers define tools, services do provider work, repositories persist data.**

**Current capability:** Google Sheets and Google Drive have registered, executable agent tools. Google Docs is present in the integration catalog/OAuth flow, but does not yet have an agent app registry or executable Docs tools.

## Tool pathway at a glance

```text
Browser + Supabase session
        │  Bearer JWT
        ▼
POST /agent/chat ──► get_current_user + database session
        │
        ▼
AgentService ──► persist user message ──► ExecutionContext(user_id, db)
        │                                         │
        ▼                                         ▼
Agent runtime / LLM ◄── unified tool definitions from agent/tools/registry.py
        │  chooses { tool name, arguments }
        ▼
dispatcher.execute_tool
  1. finds registered tool
  2. validates LLM arguments with Pydantic
  3. resolves only that tool's service dependency
  4. calls the small tool handler
        │
        ▼
Tool handler ──► SpreadsheetService or DriveService ──► Google API
                       │
                       ▼
          GoogleCredentialFactory checks enabled installation,
          reads encrypted connection tokens, refreshes if necessary
        │
        ▼
Tool result returns to LLM ──► final assistant message persisted ──► HTTP response
```

## Fast orientation

| Concern | Entry point | Owns |
| --- | --- | --- |
| HTTP and auth | `app/api/routers/` | Endpoints, request/response schemas, JWT dependency |
| Application workflow | `app/services/` | Chat orchestration and integration lifecycle |
| Durable data | `app/repositories/` | SQLAlchemy queries and commits |
| Agent loop | `agent/core/` | LLM turns, tool selection, dispatch |
| Tool contract | `integrated_apps/*/tools/` | Pydantic arguments and thin handlers |
| Provider operation | `*_service.py`, `*_client.py` | Google Sheets/Drive calls |
| Per-request wiring | `agent/dependencies/resolver.py` | Builds only the service the selected tool needs |

## 1. Authentication and request context

Every protected endpoint depends on `get_current_user` in `app/api/dependencies.py`.

1. The frontend gets a Supabase access token after sign-in.
2. It sends `Authorization: Bearer <token>` to the FastAPI API.
3. `SupabaseAuthProvider` verifies that token with Supabase and produces `UserResponse`.
4. `get_db` creates a SQLAlchemy session for this request.
5. The router passes the verified user and database session to its service.

The agent never accepts a `user_id` from the LLM or browser request body. `user_id` comes only from the verified JWT and is carried in `ExecutionContext`.

```text
JWT → get_current_user → UserResponse.id → ExecutionContext.user_id
```

## 2. Chat request to tool execution

### HTTP boundary

`POST /agent/chat` is implemented in `app/api/routers/agent_router.py`.

```json
{
  "message": "Find my project spreadsheets"
}
```

The router calls `AgentService.agent_chat_request_service(...)` with the verified user ID and request-scoped database session.

### Conversation persistence

`AgentService` in `app/services/agent_service.py`:

1. Creates a conversation if `conversation_id` is absent, or verifies that an existing conversation belongs to the user.
2. Persists the user message through `message_repo`.
3. Loads recent message history and converts ORM models into the agent's message DTOs.
4. Creates `ExecutionContext(user_id, db)` and calls `agent_runtime`.
5. Persists the assistant and tool-call messages returned by the agent loop.

This keeps chat history in PostgreSQL while the LLM and tool code use clean, framework-independent models.

### Agent loop and dispatcher

`agent/core/loop.py` sends the current conversation plus the unified tool list to the LLM. If the LLM returns a tool call, it passes it to `agent/core/dispatcher.py`.

The dispatcher is the execution gate:

1. Looks up the tool by name in `agent/tools/registry.py`.
2. Validates generated arguments with that tool's Pydantic `args_schema`.
3. Resolves declared dependencies using `agent/dependencies/resolver.py`.
4. Calls `handler(**dependencies, **validated_args)`.
5. Converts the result into a tool message for the next LLM turn.

The dispatcher **executes** the selected tool, but it does not know Google Sheets, Drive, OAuth, or SQL details. That is deliberate: it remains generic for every future integrated app.

## 3. Tool handler versus service

Tool modules under `integrated_apps/google/*/tools/` are the agent-facing interface. They define:

- a Pydantic input schema;
- a description used in the LLM tool definition;
- a small function that passes validated inputs to its injected service.

They do **not** take `user_id`, open database sessions, decrypt tokens, or implement Google API calls.

Services are the provider-facing layer:

- `SpreadsheetService` performs Sheets discovery, metadata, reads, writes, analysis, and sheet management;
- `DriveService` performs Drive discovery and metadata operations;
- `SheetClient` and `DriveClient` contain low-level Google client construction/use.

```text
dispatcher → handler in tools/ → app service → provider client → Google API
```

The service is constructed with the request's authenticated identity once. This means every tool invocation is automatically scoped to the right user without trusting LLM-supplied identity data.

## 4. Tool registration and dependency injection

Each app publishes a registry:

- Sheets: `integrated_apps/google/spreadsheet_app/spreadsheet_registry.py`
- Drive: `integrated_apps/google/drive_app/drive_registry.py`

Each registered tool contains:

```python
RegisteredTool(
    definition=ToolDefinition(...),     # sent to the LLM
    args_schema=MyToolArguments,        # validates LLM arguments
    handler=my_tool_handler,            # thin tool boundary
    dependencies=("drive_service",),   # request-scoped service requirement
)
```

`agent/tools/registry.py` merges all app registries and rejects duplicate names. `DependencyResolver` maps dependency names to provider functions:

| Dependency | Provider | Result |
| --- | --- | --- |
| `spreadsheet_service` | `build_spreadsheet_service(ctx)` | A Sheets service bound to this user and DB session |
| `drive_service` | `build_drive_service(ctx)` | A Drive service bound to this user and DB session |

Providers create `GoogleCredentialFactory(db=ctx.db, integration_key=...)`. The factory requires the matching app installation to be connected and enabled before returning credentials.

The registry dependency name selects the provider; the resolver injects its result into the handler as `service`. This keeps every handler signature consistent: `def handler(service, ...)`.

## 5. Google connection and persistence flow

The integration frontend talks to `app/api/routers/integrations_router.py`.

| Endpoint | Purpose |
| --- | --- |
| `GET /integrator/catalog` | Lists Sheets, Drive, and Docs with the current user's app status |
| `GET /integrator/google/connect/{integration_key}` | Creates a Google OAuth URL for one app |
| `GET /integrator/google/callback` | Exchanges authorization code, persists connection, and redirects to frontend |
| `PUT /integrator/{integration_key}/enabled` | Enables or pauses one installed app |
| `DELETE /integrator/{integration_key}` | Disables one installed app without revoking the shared Google connection |

### OAuth lifecycle

```text
Frontend requests connect URL
  → IntegrationService selects scopes from GOOGLE_APP_SCOPES
  → GoogleAuth creates state + PKCE verifier
  → Redis stores one-time state for 10 minutes
  → browser consents at Google
  → Google calls /integrator/google/callback
  → state is consumed once, code is exchanged
  → encrypted provider connection + app installation are saved in one DB transaction
  → browser returns to frontend
```

`app/integrations/google/scopes_config.py` is the single scope catalog. It drives the OAuth request and the frontend-visible integration catalog.

### Database ownership model

| Table | Role |
| --- | --- |
| `users` | Local application user, keyed by Supabase user UUID |
| `conversations` | User-owned chat sessions |
| `messages` | User, assistant, and tool messages for a conversation |
| `integrations` | One encrypted shared Google provider connection per user |
| `integration_installations` | Per-app status, enabled flag, requested scopes, and granted scopes |

The shared connection allows Sheets and Drive to reuse one Google account token. `integration_installations` prevents a connected token from making an app available unless that specific app is enabled.

Token values are encrypted in `IntegrationRepo` using `OAUTH_TOKEN_ENCRYPTION_KEY`. They are never returned by the integration API or exposed to the frontend.

Apply the required integration migration once for a new local database:

```bash
psql -h localhost -U postgres -d postgres -f migrations/20261024_create_integration_installations.sql
```

## 6. Adding another integrated app

Use this sequence to keep responsibilities clean:

1. Add the app key and minimum scopes to `GOOGLE_APP_SCOPES`.
2. Add the user-facing label in `INTEGRATION_LABELS`.
3. Create `integrated_apps/google/<app>_app/` with client, service, provider, tools, and registry.
4. Register tools with unique names and one dependency name.
5. Add the service provider to `agent/dependencies/resolver.py`.
6. Merge the app registry in `agent/tools/registry.py`.
7. Reuse the generic integration endpoints; no new OAuth router is required.
8. Add a migration only if new persistence is needed.

Do not put provider calls in the dispatcher or use browser/LLM-provided user IDs in handlers. That bypasses the architecture's request scoping and authorization boundary.

## Local run

Required environment values belong in `.env` and must not be committed:

```env
SUPABASE_URL=
SUPABASE_KEY=
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/integrator/google/callback
REDIS_URL=redis://localhost:6379/0
OAUTH_TOKEN_ENCRYPTION_KEY=
```

Run the services:

```bash
.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
.venv/bin/python -m http.server 5173 --bind 127.0.0.1 --directory frontend
```

Open `http://localhost:5173`.
