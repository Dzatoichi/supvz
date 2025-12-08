package com.supvz.notifications_service.core.exception;

public class NotificationIsNotSentException extends RuntimeException {
    public NotificationIsNotSentException(String message) {
        super(message);
    }
}
