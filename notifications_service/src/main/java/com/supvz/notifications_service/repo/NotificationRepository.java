package com.supvz.notifications_service.repo;

import com.supvz.notifications_service.model.entity.Notification;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

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
}