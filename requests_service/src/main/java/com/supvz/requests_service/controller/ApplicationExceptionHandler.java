package com.supvz.requests_service.controller;

import com.supvz.requests_service.core.exception.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindException;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.support.DefaultHandlerExceptionResolver;

import java.util.Map;

/**
 * Advice-контроллер для обработки исключений и последующих респонсов.
 */
@Slf4j
@RestControllerAdvice
public class ApplicationExceptionHandler extends DefaultHandlerExceptionResolver {
    /**
     * Обработка исключения при отсутствии валидации.
     */
    @ExceptionHandler(BindException.class)
    public ResponseEntity<?> handleBindException(BindException ex) {
        HttpStatus status = HttpStatus.BAD_REQUEST;
        Map<String, Object> body = Map.of("status", status.value(), "message", ex.getBindingResult().getAllErrors().stream().map(ObjectError::getDefaultMessage).toList());
        return ResponseEntity.badRequest().body(body);
    }

    /**
     * Обработка исключения при отсутствии запроса для мастера.
     */
    @ExceptionHandler
    public ResponseEntity<?> handleRequestNotFoundException(RequestNotFoundException ex) {
        log.warn(ex.getMessage());
        HttpStatus status = HttpStatus.BAD_REQUEST;
        Map<String, Object> body = Map.of("status", status.value(), "message", ex.getMessage());
        return ResponseEntity.badRequest().body(body);
    }

    /**
     * Обработка исключения при отсутствии обращения мастера на запрос.
     */
    @ExceptionHandler
    public ResponseEntity<?> handleRequestAssignmentNotFoundException(RequestAssignmentNotFoundException ex) {
        log.warn(ex.getMessage());
        HttpStatus status = HttpStatus.BAD_REQUEST;
        Map<String, Object> body = Map.of("status", status.value(), "message", ex.getMessage());
        return ResponseEntity.badRequest().body(body);
    }


    /**
     * Обработка исключения при конфликте с обращением на заявку.
     * <br/>
     * Например, обращение на заявку уже было однажды создано.
     */
    @ExceptionHandler(RequestAssignmentConflictException.class)
    public ResponseEntity<?> handleRequestAssignmentConflictException(RequestAssignmentConflictException ex) {
        log.warn(ex.getMessage());
        HttpStatus status = HttpStatus.CONFLICT;
        Map<String, Object> body = Map.of("status", status.value(), "message", ex.getMessage());
        return ResponseEntity.status(status).body(body);
    }

    /**
     * Обработка исключения при конфликте с заявкой.
     * <br/>
     * Например, заявка выполнена или отклонена, а мастер пытается изменить ее статус.
     */
    @ExceptionHandler(RequestConflictException.class)
    public ResponseEntity<?> handleRequestConflictException(RequestConflictException ex) {
        log.warn(ex.getMessage());
        HttpStatus status = HttpStatus.CONFLICT;
        Map<String, Object> body = Map.of("status", status.value(), "message", ex.getMessage());
        return ResponseEntity.status(status).body(body);
    }

    /**
     * Обработка исключения при неправильной полезной нагрузке обращения на заявку.
     * <br/>
     * Например, обращение на заявку с типом {@code AssignnmentAction.system_cancel}.
     * Данный тип может выставлять лишь система.
     */
    @ExceptionHandler(RequestAssignmentInvalidPayloadException.class)
    public ResponseEntity<?> handleRequestAssignmentInvalidPayloadException(RequestAssignmentInvalidPayloadException ex) {
        log.warn(ex.getMessage());
        HttpStatus status = HttpStatus.BAD_REQUEST;
        Map<String, Object> body = Map.of("status", status.value(), "message", ex.getMessage());
        return ResponseEntity.badRequest().body(body);
    }
}