package com.supvz.requests_service.core.exception;

public class RequestConflictException extends RuntimeException {
    public RequestConflictException(String message) {
        super(message);
    }
}
