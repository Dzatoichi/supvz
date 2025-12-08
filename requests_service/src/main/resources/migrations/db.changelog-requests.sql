--liquibase formatted sql

--changeset re1kur:1
CREATE TABLE IF NOT EXISTS requests
(
    id BIGSERIAL PRIMARY KEY,
    pvz_id INT NOT NULL,
    appellant_id BIGINT NOT NULL,
    subject VARCHAR(64),
    description TEXT NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'assigned', 'rejected', 'completed')),
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

--changeset re1kur:2
CREATE TABLE IF NOT EXISTS request_assignments
(
    id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL,
    handyman_id BIGINT NOT NULL,
    action VARCHAR(16) NOT NULL DEFAULT 'assign' CHECK (action IN ('cancel', 'assign', 'reject', 'complete')),
    processed_at TIMESTAMP,
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    FOREIGN KEY (request_id) REFERENCES requests(id) ON DELETE CASCADE,
    UNIQUE (request_id, handyman_id)
);

--changeset re1kur:3
CREATE INDEX IF NOT EXISTS idx_assignments_request_id ON request_assignments (request_id);
CREATE INDEX IF NOT EXISTS idx_requests_pvz_id_status ON requests (pvz_id, status);
CREATE INDEX IF NOT EXISTS idx_assignments_handyman_id ON request_assignments (handyman_id);