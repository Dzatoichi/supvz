package com.supvz.requests_service.controller;

import com.supvz.requests_service.core.RequestAssignmentNotFoundException;
import com.supvz.requests_service.core.RequestNotFoundException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindException;
import org.springframework.validation.ObjectError;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Map;

@Slf4j
@RestControllerAdvice
public class ControllerAdvice {
    @ExceptionHandler(BindException.class)
    public ResponseEntity<?> handleBindException(BindException ex) {
        HttpStatus status = HttpStatus.BAD_REQUEST;
        Map<String, Object> body = Map.of("status", status.value(), "message", ex.getBindingResult().getAllErrors().stream().map(ObjectError::getDefaultMessage));
        return ResponseEntity.badRequest().body(body);
    }

    @ExceptionHandler
    public ResponseEntity<?> handleRequestNotFoundException(RequestNotFoundException ex) {
        log.info(ex.getMessage());

        HttpStatus status = HttpStatus.BAD_REQUEST;
        Map<String, Object> body = Map.of("status", status.value(), "message", ex.getMessage());

        return ResponseEntity.badRequest().body(body);
    }

    @ExceptionHandler
    public ResponseEntity<?> handleRequestAssignmentNotFoundException(RequestAssignmentNotFoundException ex) {
        log.info(ex.getMessage());

        HttpStatus status = HttpStatus.BAD_REQUEST;
        Map<String, Object> body = Map.of("status", status.value(), "message", ex.getMessage());

        return ResponseEntity.badRequest().body(body);
    }
}
