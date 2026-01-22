package com.supvz.notifications_service.controller;

import com.supvz.notifications_service.core.exception.NotificationNotFoundException;
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
public class NotificationsExceptionHandler extends ResponseEntityExceptionHandler {
    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, Object>> handleOtherExceptions(
            RuntimeException ex
    ) {
        log.error("Непредвиденная ошибка: [{}].", ex.getMessage());
        Map<String, Object> body = Map.of("status", HttpStatus.INTERNAL_SERVER_ERROR, "message", "Непредвиденная ошибка.");
        return ResponseEntity.internalServerError().body(body);
    }

    @ExceptionHandler(JDBCConnectionException.class)
    public ResponseEntity<Map<String, Object>> handleJDBCConnectionException(
            JDBCConnectionException ex
    ) {
        log.error("Ошибка при подключении к БД: {}", ex.getMessage());
        Map<String, Object> body = Map.of("status", HttpStatus.INTERNAL_SERVER_ERROR, "message", "database is unavailable.");
        return ResponseEntity.internalServerError().body(body);
    }

    @ExceptionHandler(NotificationNotFoundException.class)
    public ResponseEntity<Map<String, Object>> handleNotificationNotFoundException(
            NotificationNotFoundException ex
    ) {
        log.warn(ex.getMessage());
        Map<String, Object> body = Map.of("status", HttpStatus.BAD_REQUEST, "message", ex.getMessage());
        return ResponseEntity.badRequest().body(body);
    }
}