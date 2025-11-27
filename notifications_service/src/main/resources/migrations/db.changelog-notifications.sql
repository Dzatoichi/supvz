--liquibase formatted sql

--changeset re1kur:1
CREATE TABLE IF NOT EXISTS inbox
(
	event_id UUID PRIMARY KEY,
	event_type VARCHAR(16) NOT NULL CHECK (event_type IN ('notification', 'other')),
	payload TEXT NOT NULL,
	reserved_to TIMESTAMP,
	processed_at TIMESTAMP,
	processed BOOLEAN NOT NULL DEFAULT FALSE,
	clean_after TIMESTAMP,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
	updated_at TIMESTAMP NOT NULL DEFAULT now()
);

--changeset re1kur:2
CREATE TABLE IF NOT EXISTS notifications
(
	id BIGSERIAL PRIMARY KEY,
	event_id UUID NOT NULL UNIQUE,
	notification_type VARCHAR(16) NOT NULL CHECK (notification_type IN ('email', 'web', 'push')),
	recipient_id VARCHAR(256) NOT NULL,
	body TEXT,
	subject VARCHAR(256),
	sent_at TIMESTAMP,
	sent BOOLEAN NOT NULL DEFAULT FALSE,
	viewed BOOLEAN,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
	updated_at TIMESTAMP NOT NULL DEFAULT now(),
	FOREIGN KEY (event_id) REFERENCES inbox (event_id) ON DELETE CASCADE
);

--changeset re1kur:3
CREATE INDEX IF NOT EXISTS idx_notifications_recipient
    ON notifications (recipient_id);

CREATE INDEX IF NOT EXISTS idx_inbox_processing
    ON inbox (reserved_to, created_at)
    WHERE processed = FALSE;

CREATE INDEX IF NOT EXISTS idx_inbox_failed_cleanup
    ON inbox (clean_after, processed)
    WHERE processed = FALSE
    AND clean_after IS NOT NULL;