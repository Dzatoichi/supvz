\c postgres
CREATE EXTENSION IF NOT EXISTS pg_cron;

\c auth_db

ALTER SYSTEM SET cron.database_name = 'auth_db';
SELECT pg_reload_conf();

GRANT USAGE ON SCHEMA cron TO postgres;