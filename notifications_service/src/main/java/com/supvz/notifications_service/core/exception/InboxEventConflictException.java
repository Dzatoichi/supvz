package com.supvz.notifications_service.core.exception;

public class InboxEventConflictException extends RuntimeException {
    public InboxEventConflictException(String message) {
        super(message);
    }
}
