package com.supvz.notifications_service.controller;

import lombok.extern.slf4j.Slf4j;
import org.hibernate.exception.JDBCConnectionException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import java.util.Map;

@Slf4j
@RestControllerAdvice
public class ControllerAdvice extends ResponseEntityExceptionHandler {
    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, Object>> handleOtherExceptions(RuntimeException ex) {
        log.error("Unexpected error: [{}].", ex.getMessage());
        Map<String, Object> body = Map.of("status", HttpStatus.INTERNAL_SERVER_ERROR, "message", "Unexpected error.");
        return ResponseEntity.internalServerError().body(body);
    }

    @ExceptionHandler(JDBCConnectionException.class)
    public ResponseEntity<Map<String, Object>> handleJDBCConnectionException() {
        Map<String, Object> body = Map.of("status", HttpStatus.INTERNAL_SERVER_ERROR, "message", "database is unavailable.");
        return ResponseEntity.internalServerError().body(body);
    }
}