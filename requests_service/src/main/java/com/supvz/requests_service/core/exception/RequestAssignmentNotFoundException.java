package com.supvz.requests_service.core.exception;

/*
Исключение отсутствия ответа на запрос.
 */
public class RequestAssignmentNotFoundException extends RuntimeException {
    public RequestAssignmentNotFoundException(String message) {
        super(message);
    }
}
