package com.supvz.notifications_service.repo;

import com.supvz.notifications_service.model.entity.Notification;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface NotificationRepository extends CrudRepository<Notification, Long>, JpaSpecificationExecutor<Notification> {
    @Query(value = """
            FROM Notification n
            WHERE n.event.eventId = :id
            """)
    Optional<Notification> findByEventId(
            @Param("id") UUID id);

    @Query(value = """
            DELETE FROM notifications WHERE
            (viewed = TRUE AND sent_at < now() - (:viewedTtl * INTERVAL '1 day')) OR
            (viewed = FALSE AND sent_at < now() - (:notViewedTtl * INTERVAL '1 day')) OR
            (notification_type = 'email' AND sent_at < now() - (:emailTtl * INTERVAL '1 day'))
            RETURNING id;
            """, nativeQuery = true)
    List<Integer> deleteOldNotifications(
            @Param("viewedTtl") int viewedTtlDays,
            @Param("notViewedTtl") int notViewedTtlDays,
            @Param("emailTtl") int emailTtlDays
    );
}