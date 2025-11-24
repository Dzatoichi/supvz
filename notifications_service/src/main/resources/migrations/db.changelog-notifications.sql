--liquibase formatted sql

--changeset re1kur:1
--preconditions onFail:MARK_RAN
--precondition-sql-check expectedResult:0 SELECT COUNT(*) FROM pg_type WHERE typname = 'notification_type';
CREATE TYPE notification_type AS ENUM (
    'email',
    'web',
    'push'
);

--changeset re1kur:2
--preconditions onFail:MARK_RAN
--precondition-sql-check expectedResult:0 SELECT COUNT(*) FROM pg_type WHERE typname = 'event_type';
CREATE TYPE event_type AS ENUM (
    'notification',
    'other'
);

--changeset re1kur:3
CREATE TABLE IF NOT EXISTS inbox
(
	event_id UUID PRIMARY KEY,
	event_type event_type NOT NULL,
	payload TEXT NOT NULL,
	reserved_to TIMESTAMP,
	processed_at TIMESTAMP,
	processed BOOLEAN NOT NULL DEFAULT FALSE,
	clean_after TIMESTAMP,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
	updated_at TIMESTAMP NOT NULL DEFAULT now()
);

--changeset re1kur:4
CREATE TABLE IF NOT EXISTS notifications
(
	id BIGSERIAL PRIMARY KEY,
	event_id UUID NOT NULL UNIQUE,
	notification_type notification_type NOT NULL,
	recipient_id VARCHAR(256) NOT NULL,
	body TEXT,
	subject VARCHAR(256),
	sent_at TIMESTAMP,
	sent BOOLEAN NOT NULL DEFAULT FALSE,
	viewed BOOLEAN,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
	updated_at TIMESTAMP NOT NULL DEFAULT now(),
	FOREIGN KEY(event_id) REFERENCES inbox (event_id) ON DELETE CASCADE
);

--changeset re1kur:5
CREATE INDEX IF NOT EXISTS idx_inbox_events_unprocessed ON inbox (created_at) WHERE processed = FALSE;
CREATE INDEX IF NOT EXISTS idx_inbox_events_failed ON inbox (clean_after) WHERE processed = FALSE;
CREATE INDEX IF NOT EXISTS idx_notifications_recipient ON notifications (recipient_id);
CREATE INDEX IF NOT EXISTS idx_inbox_unprocessed_reservation ON inbox (processed, reserved_to) WHERE processed = FALSE;
CREATE INDEX IF NOT EXISTS idx_inbox_failed ON inbox (clean_after) WHERE clean_after IS NOT NULL;


--    todo: индексы подумать