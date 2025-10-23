package com.supvz.requests_service.core;

/*
Исключение отсутствия запроса.
 */
public class RequestNotFoundException extends RuntimeException {
    public RequestNotFoundException(String message) {
        super(message);
    }
}
