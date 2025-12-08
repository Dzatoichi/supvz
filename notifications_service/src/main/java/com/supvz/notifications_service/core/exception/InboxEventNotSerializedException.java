package com.supvz.notifications_service.core.exception;

public class InboxEventNotSerializedException extends RuntimeException {
    public InboxEventNotSerializedException(String message) {
        super(message);
    }
}
