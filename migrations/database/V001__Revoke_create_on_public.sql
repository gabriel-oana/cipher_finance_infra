-- Revoke create privileges on the public schema.
-- The only objects we want available via the public schema are functions.
REVOKE CREATE ON SCHEMA public FROM PUBLIC;

