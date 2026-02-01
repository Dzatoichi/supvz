\c postgres
CREATE EXTENSION IF NOT EXISTS pg_cron;

\c shifts_db

ALTER SYSTEM SET cron.database_name = 'shifts_db';
SELECT pg_reload_conf();

-- Задача 1: Отмена просроченных pending запросов (каждые 5 минут)
-- Отменяет запросы, у которых смена уже началась
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM cron.job WHERE jobname = 'cancel-expired-pending-requests'
    ) THEN
        PERFORM cron.schedule(
            'cancel-expired-pending-requests',
            '*/5 * * * *',
            $$
            UPDATE shift_requests
            SET status = 'cancelled_by_system',
                processed_at = NOW(),
                reason = 'Автоматическая отмена: смена уже началась'
            WHERE status = 'pending'
              AND scheduled_shift_start_time <= NOW()
            $$
        );
        RAISE NOTICE 'Cron job for cancel expired pending requests created';
    ELSE
        RAISE NOTICE 'Cron job cancel-expired-pending-requests already exists';
    END IF;
END
$$;

-- Задача 2: Очистка старых запросов (каждое воскресенье в 03:00)
-- Удаляет запросы старше 2 месяцев (кроме approved)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM cron.job WHERE jobname = 'cleanup-old-shift-requests'
    ) THEN
        PERFORM cron.schedule(
            'cleanup-old-shift-requests',
            '0 3 * * 0',
            $$
            DELETE FROM shift_requests
            WHERE status != 'approved'
              AND created_at < NOW() - INTERVAL '2 months'
            $$
        );
        RAISE NOTICE 'Cron job for cleanup old shift requests created';
    ELSE
        RAISE NOTICE 'Cron job cleanup-old-shift-requests already exists';
    END IF;
END
$$;
