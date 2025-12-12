package com.supvz.notifications_service.util;

import com.supvz.notifications_service.model.entity.Notification;
import com.supvz.notifications_service.model.entity.NotificationType;
import org.springframework.data.jpa.domain.Specification;

import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Вспомогательный класс для создания динамических запросов с фильтрацией.
 */
public class NotificationSpecifications {
    public static Specification<Notification> hasEventId(UUID eventId) {
        return (root, query, cb) -> {
            if (eventId == null) return cb.conjunction();
            return cb.equal(root.get("eventId"), eventId);
        };
    }

    public static Specification<Notification> hasRecipientId(String recipientId) {
        return (root, query, cb) -> {
            if (recipientId == null) return null;
            return cb.equal(root.get("recipientId"), recipientId);
        };
    }

    public static Specification<Notification> likeSubject(String subject) {
        return (root, query, cb) -> {
            if (subject == null) return cb.conjunction();
            return cb.like(root.get("subject"), subject);
        };
    }

    public static Specification<Notification> likeBody(String body) {
        return (root, query, cb) -> {
            if (body == null) return cb.conjunction();
            return cb.like(root.get("body"), body);
        };
    }

    public static Specification<Notification> hasType(NotificationType type) {
        return (root, query, cb) -> {
            if (type == null) return cb.conjunction();
            return cb.equal(root.get("notificationType"), type);
        };
    }

    public static Specification<Notification> isSent(Boolean isSent) {
        return (root, query, cb) -> {
            if (isSent == null) return cb.conjunction();
            return cb.equal(root.get("sent"), isSent);
        };
    }

    public static Specification<Notification> isViewed(Boolean viewed) {
        return (root, query, cb) -> {
            if (viewed == null) return cb.conjunction();
            return cb.equal(root.get("viewed"), viewed);
        };
    }

    public static Specification<Notification> betweenDates(LocalDateTime startDate, LocalDateTime endDate) {
        return (root, query, cb) -> {
            if (startDate == null || endDate == null) return cb.conjunction();
            return cb.between(root.get("sentAt"), startDate, endDate);
        };
    }
}