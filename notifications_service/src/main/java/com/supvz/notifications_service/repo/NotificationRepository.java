package com.supvz.notifications_service.repo;

import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.model.entity.NotificationType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface NotificationRepository extends CrudRepository<Notification, Long> {
    @Query(value = """
            FROM Notification n
            WHERE n.event.eventId = :id
            """)
    Optional<Notification> findByEventId(
            @Param("id") UUID id);

    @Query("""
            FROM Notification n WHERE
            (:recipientId IS NULL OR n.recipientId = :recipientId) AND
            (:eventId IS NULL OR n.event.id = :eventId) AND
            (:type IS NULL OR n.notificationType = :type) AND
            (:viewed IS NULL OR n.viewed = :viewed) AND
            n.sentAt BETWEEN :startDate AND :endDate AND
            n.sent IS TRUE
            """)
    Page<Notification> findAllWithDateFilter(
            Pageable pageable,
            @Param("recipientId") String recipientId,
            @Param("eventId") UUID eventId,
            @Param("type") NotificationType type,
            @Param("viewed") Boolean viewed,
            @Param("startDate") LocalDateTime startDate,
            @Param("endDate") LocalDateTime endDate
    );

    @Query("""
            FROM Notification n WHERE
            (:recipientId IS NULL OR n.recipientId = :recipientId) AND
            (:eventId IS NULL OR n.event.id = :eventId) AND
            (:type IS NULL OR n.notificationType = :type) AND
            (:viewed IS NULL OR n.viewed = :viewed) AND
            n.sent IS TRUE
            """)
    Page<Notification> findAll(
            Pageable pageable,
            @Param("recipientId") String recipientId,
            @Param("eventId") UUID eventId,
            @Param("type") NotificationType type,
            @Param("viewed") Boolean viewed
    );
}