package com.supvz.requests_service.controller;

import com.supvz.requests_service.core.exception.RequestAssignmentNotFoundException;
import com.supvz.requests_service.core.exception.RequestNotFoundException;
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
//    todo: Появились новые исключения. Написать по ним тесты и handler'ы.
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
     * Обработка исключения при отсутствии ответа мастера на запрос.
     */
    @ExceptionHandler
    public ResponseEntity<?> handleRequestAssignmentNotFoundException(RequestAssignmentNotFoundException ex) {
        log.warn(ex.getMessage());
        HttpStatus status = HttpStatus.BAD_REQUEST;
        Map<String, Object> body = Map.of("status", status.value(), "message", ex.getMessage());
        return ResponseEntity.badRequest().body(body);
    }
}