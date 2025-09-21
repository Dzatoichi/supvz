\c postgres
CREATE EXTENSION IF NOT EXISTS pg_cron;

\c auth_db

ALTER SYSTEM SET cron.database_name = 'auth_db';
SELECT pg_reload_conf();

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM cron.job WHERE jobname = 'delete-expired-tokens'
    ) THEN
        PERFORM cron.schedule(
            'delete-expired-tokens',
            '0 0 * * 0',
            'DELETE FROM refresh_tokens WHERE expires_at < NOW()'
        );
        RAISE NOTICE 'Cron job for token cleanup created';
    ELSE
        RAISE NOTICE 'Cron job already exists';
    END IF;
END
$$;