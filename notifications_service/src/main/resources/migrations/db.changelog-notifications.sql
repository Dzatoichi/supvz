--liquibase formatted sql

--changeset re1kur:1
--preconditions onFail:MARK_RAN
--precondition-sql-check expectedResult:0 SELECT COUNT(*) FROM pg_type WHERE typname = 'notification_type';
CREATE TYPE notification_type AS ENUM (
    'email',
    'sms',
    'push'
);

--changeset re1kur:2
CREATE TABLE IF NOT EXISTS inbox_events
(
	event_id UUID PRIMARY KEY,
	event_type notification_type NOT NULL,
	reserved_to TIMESTAMP,
	payload TEXT NOT NULL,
	created_at TIMESTAMP NOT NULL,
	received_at TIMESTAMP NOT NULL DEFAULT now(),
	processed_at TIMESTAMP,
	processed BOOLEAN NOT NULL DEFAULT FALSE
);

--changeset re1kur:3
CREATE TABLE IF NOT EXISTS notifications
(
	id BIGSERIAL PRIMARY KEY,
	event_id UUID NOT NULL UNIQUE,
	notification_type notification_type NOT NULL,
	recipient_id VARCHAR(256) NOT NULL,
	body TEXT,
	subject VARCHAR(256),
	created_at TIMESTAMP NOT NULL DEFAULT now(),
	sent_at TIMESTAMP,
	FOREIGN KEY(event_id) REFERENCES inbox_events(event_id) ON DELETE CASCADE
);

--changeset re1kur:4
CREATE INDEX IF NOT EXISTS idx_inbox_events_unprocessed ON inbox_events (received_at) WHERE processed = FALSE;
CREATE INDEX IF NOT EXISTS idx_notifications_recipient ON notifications (recipient_id);