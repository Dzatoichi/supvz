package com.supvz.notifications_service.repo;

import com.supvz.notifications_service.model.entity.InboxEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Repository
public interface InboxEventRepository extends JpaRepository<InboxEvent, UUID> {
    @Query(value = """
            WITH batch AS (
            SELECT event_id FROM inbox
            WHERE processed IS FALSE
            AND (reserved_to IS NULL OR reserved_to < now())
            AND (clean_after IS NULL OR clean_after > now())
            ORDER BY created_at ASC
            LIMIT :batchSize
            )
            UPDATE inbox
            SET reserved_to = :reservedTo
            WHERE event_id IN (SELECT event_id FROM batch)
            RETURNING event_id
            """, nativeQuery = true)
    List<UUID> findAndReserveUnprocessedInBatch(
            @Param("batchSize") int batchSize,
            @Param("reservedTo") LocalDateTime reservedTo);

    @Query(value = """
            INSERT INTO inbox (event_id, event_type, payload)
            VALUES (:eventId, :eventType, :payload)
            ON CONFLICT (event_id) DO NOTHING
            RETURNING *
            """, nativeQuery = true)
    InboxEvent saveIfNotExists(
            @Param("eventId") UUID eventId,
            @Param("eventType") String eventType,
            @Param("payload") String payload);

    @Query(value = """
            WITH batch AS (
            SELECT event_id FROM inbox i
            WHERE i.processed IS FALSE
            AND (i.reserved_to IS NULL OR i.reserved_to < now())
            AND (i.clean_after IS NOT NULL AND i.clean_after < now())
            ORDER BY i.clean_after
            LIMIT :batchSize
            )
            DELETE FROM inbox i
            WHERE i.event_id IN (SELECT event_id FROM batch)
            RETURNING i.event_id
            """, nativeQuery = true)
    List<UUID> deleteFailedInBatch(Integer batchSize);
}
