--liquibase formatted sql

--changeset re1kur:1
CREATE TABLE IF NOT EXISTS requests
(
    id BIGSERIAL PRIMARY KEY,
    pvz_id INT NOT NULL,
    appellant_id BIGINT NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'assigned', 'rejected', 'completed')),
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);
-- TODO: статус заявки.

--changeset re1kur:2
CREATE TABLE IF NOT EXISTS request_assignments
(
    id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL,
    handyman_id BIGINT NOT NULL,
    type VARCHAR(16) NOT NULL DEFAULT 'assign' CHECK (status IN ('cancel', 'assign', 'reject', 'complete')),
    processed_at TIMESTAMP,
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
    FOREIGN KEY (request_id) REFERENCES requests(id) ON DELETE CASCADE,
    UNIQUE (request_id, handyman_id)
);

-- TODO: индексы