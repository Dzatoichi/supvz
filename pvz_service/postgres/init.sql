CREATE EXTENSION IF NOT EXISTS pg_cron;

GRANT USAGE ON SCHEMA cron TO PUBLIC;

-- Процедура батчевого удаления
CREATE OR REPLACE PROCEDURE cleanup_inbox_events(
    retention_days INT DEFAULT 15,
    batch_size INT DEFAULT 1000
)
    LANGUAGE plpgsql
AS
$$
DECLARE
    deleted_count INT;
    total_deleted INT := 0;
BEGIN
    LOOP
        DELETE
        FROM inbox_events
        WHERE event_id IN (SELECT event_id
                           FROM inbox_events
                           WHERE finished_at < NOW() - (retention_days || ' days')::INTERVAL
                           LIMIT batch_size);

        GET DIAGNOSTICS deleted_count = ROW_COUNT;
        total_deleted := total_deleted + deleted_count;

        EXIT WHEN deleted_count < batch_size;

        COMMIT;
    END LOOP;

    RAISE LOG 'inbox_events cleanup: deleted % rows', total_deleted;
END;
$$;

-- Регистрация cron-задачи
DO
$$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM cron.job WHERE jobname = 'cleanup-inbox-events') THEN
            PERFORM cron.schedule(
                    'cleanup-inbox-events',
                    '0 3 * * *',
                    'CALL cleanup_inbox_events(15, 1000)'
                    );
            RAISE NOTICE 'Created cron job: cleanup-inbox-events';
        END IF;
    END
$$;