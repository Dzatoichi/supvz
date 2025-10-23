--liquibase formatted sql

--changeset re1kur:1
CREATE TABLE IF NOT EXISTS requests
(
    id BIGSERIAL PRIMARY KEY,
    pvz_id INT NOT NULL,
    appellant_id UUID NOT NULL,
    description TEXT NOT NULL
);

--changeset re1kur:2
CREATE TABLE IF NOT EXISTS request_assignments
(
    id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL,
    handyman_id UUID NOT NULL,
    status VARCHAR(16) NOT NULL DEFAULT 'ASSIGNED' CHECK (status IN ('ASSIGNED', 'CONFIRMED', 'REJECTED')),
    assigned_at TIMESTAMP NOT NULL DEFAULT now(),
    completed_at TIMESTAMP,
    description TEXT,
    FOREIGN KEY (request_id) REFERENCES requests(id) ON DELETE CASCADE
);