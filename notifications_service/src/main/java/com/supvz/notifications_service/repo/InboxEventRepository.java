package com.supvz.notifications_service.repo;

import com.supvz.notifications_service.entity.InboxEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Repository
public interface InboxEventRepository extends JpaRepository<InboxEvent, UUID> {
    @Query(value = """
            FROM InboxEvent i WHERE
            i.processed IS FALSE
            AND (i.reservedTo IS NULL OR i.reservedTo < CURRENT_TIMESTAMP)
            ORDER BY receivedAt
            LIMIT :number
            """)
    List<InboxEvent> findAllUnprocessed(
            @Param("number") int number);

    @Modifying
    @Query(value = """
            UPDATE InboxEvent i
            SET i.reservedTo = :reservationTime
            WHERE i = :event AND
            (i.reservedTo IS NULL OR i.reservedTo < CURRENT_TIMESTAMP)
            """)
    int reserve(
            @Param("event") InboxEvent event,
            @Param("reservationTime") LocalDateTime reservationMinutes);

    @Modifying
    @Query(value = """
            INSERT INTO inbox_events (event_id, event_type, payload, created_at, received_at, processed)
                VALUES (:eventId, (:eventType)::notification_type, :payload, :createdAt, NOW(), FALSE)
                ON CONFLICT (event_id) DO NOTHING
                RETURNING event_id
            """, nativeQuery = true)
    List<UUID> saveIfNotExists(
            @Param("eventId") UUID eventId,
            @Param("eventType") String eventType,
            @Param("payload") String payload,
            @Param("createdAt") LocalDateTime createdAt);
}
