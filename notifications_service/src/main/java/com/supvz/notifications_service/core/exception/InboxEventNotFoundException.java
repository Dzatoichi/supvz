package com.supvz.notifications_service.core.exception;

public class InboxEventNotFoundException extends RuntimeException {
    public InboxEventNotFoundException(String message) {
        super(message);
    }
}
