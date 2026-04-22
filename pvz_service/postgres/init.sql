-- Индексы для оптимизации cleanup
CREATE INDEX CONCURRENTLY IF NOT EXISTS
    ix_inbox_events_finished_at_partial
ON inbox_events (finished_at)
WHERE finished_at IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS
    ix_inbox_events_stuck_processing
ON inbox_events (created_at)
WHERE finished_at IS NULL AND status = 'processing';



CREATE OR REPLACE PROCEDURE cleanup_inbox_events(
    retention_days INT DEFAULT 30,
    stuck_threshold_hours INT DEFAULT 24,
    batch_size INT DEFAULT 5000
)
    LANGUAGE plpgsql
AS
$$
DECLARE
    deleted_count INT;
    total_deleted INT := 0;
    cutoff_finished TIMESTAMPTZ;
    cutoff_stuck TIMESTAMPTZ;
BEGIN
    cutoff_finished := NOW() - (retention_days || ' days')::INTERVAL;
    cutoff_stuck := NOW() - (stuck_threshold_hours || ' hours')::INTERVAL;

    LOOP
        DELETE FROM inbox_events
        WHERE ctid IN (
            SELECT ctid
            FROM inbox_events
            WHERE
                (finished_at IS NOT NULL AND finished_at < cutoff_finished)
                OR
                (finished_at IS NULL AND status = 'processing' AND created_at < cutoff_stuck)
            LIMIT batch_size
            FOR UPDATE SKIP LOCKED
        );

        GET DIAGNOSTICS deleted_count = ROW_COUNT;
        total_deleted := total_deleted + deleted_count;

        COMMIT;

        EXIT WHEN deleted_count < batch_size;
    END LOOP;

    IF total_deleted > 0 THEN
        RAISE LOG 'inbox_events cleanup: deleted % rows', total_deleted;
    END IF;
END;
$$;



SELECT cron.unschedule('cleanup-inbox-events');

SELECT cron.schedule(
    'cleanup-inbox-events',
    '0 3 * * *',
    'CALL cleanup_inbox_events(30, 24, 5000)'
);