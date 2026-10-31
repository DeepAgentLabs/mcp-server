-- Storage for the hosted MCP service (keys, sessions, signup limits).
-- The private "mcp" schema is not exposed through the Supabase Data API.
-- Keys are stored only as SHA-256 digests; payloads are per-user tool state.
CREATE SCHEMA IF NOT EXISTS mcp;
REVOKE ALL ON SCHEMA mcp FROM PUBLIC;

CREATE TABLE IF NOT EXISTS mcp.users (
  user_id text PRIMARY KEY CHECK (length(user_id) BETWEEN 1 AND 128),
  display_name text NOT NULL,
  status text NOT NULL CHECK (status IN ('active', 'revoked')),
  key_hash text NOT NULL UNIQUE,
  created_at timestamptz NOT NULL DEFAULT now()
);

-- 0.5.0: optional per-key access policy (allow/deny globs, expires_at, task_id).
-- NULL keeps the default hosted tool surface. Re-running this file adds it.
ALTER TABLE mcp.users ADD COLUMN IF NOT EXISTS permissions jsonb;

CREATE TABLE IF NOT EXISTS mcp.sessions (
  owner_hash text PRIMARY KEY,
  payload text NOT NULL,
  expires_at timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_expires_at ON mcp.sessions (expires_at);

CREATE TABLE IF NOT EXISTS mcp.signup_counters (
  bucket text PRIMARY KEY,
  count integer NOT NULL,
  expires_at timestamptz NOT NULL
);

-- Defense in depth: only mcp_service has a policy; Data API roles see no rows.
ALTER TABLE mcp.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE mcp.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE mcp.signup_counters ENABLE ROW LEVEL SECURITY;

-- Least-privilege login used by the service. Set its password separately:
--   ALTER ROLE mcp_service WITH PASSWORD '<generated secret>';
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'mcp_service') THEN
    CREATE ROLE mcp_service LOGIN;
  END IF;
END
$$;
GRANT USAGE ON SCHEMA mcp TO mcp_service;
GRANT SELECT, INSERT, UPDATE ON mcp.users TO mcp_service;
GRANT SELECT, INSERT, UPDATE, DELETE ON mcp.sessions, mcp.signup_counters TO mcp_service;
DROP POLICY IF EXISTS service_access ON mcp.users;
DROP POLICY IF EXISTS service_access ON mcp.sessions;
DROP POLICY IF EXISTS service_access ON mcp.signup_counters;
CREATE POLICY service_access ON mcp.users TO mcp_service USING (true) WITH CHECK (true);
CREATE POLICY service_access ON mcp.sessions TO mcp_service USING (true) WITH CHECK (true);
CREATE POLICY service_access ON mcp.signup_counters TO mcp_service USING (true) WITH CHECK (true);
