-- Per-app installation state is separate from the user's shared Google connection.
CREATE TABLE IF NOT EXISTS integration_installations (
    id UUID PRIMARY KEY,
    integration_id UUID NOT NULL REFERENCES integrations(id) ON DELETE CASCADE,
    integration_key VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'connected'
        CHECK (status IN ('connected', 'disconnected', 'error')),
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    requested_scopes JSON NOT NULL DEFAULT '[]'::json,
    granted_scopes JSON NOT NULL DEFAULT '[]'::json,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_connected_at TIMESTAMPTZ,
    disconnected_at TIMESTAMPTZ,
    CONSTRAINT uq_connection_integration_app UNIQUE (integration_id, integration_key)
);

CREATE INDEX IF NOT EXISTS ix_integration_installations_integration_id
    ON integration_installations (integration_id);
