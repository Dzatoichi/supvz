package com.supvz.requests_service.controller;

import com.supvz.requests_service.model.dto.RequestDto;
import com.supvz.requests_service.model.dto.RequestUpdatePayload;
import com.supvz.requests_service.service.RequestService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * REST-контроллер для обработки заявки.
 */
@RestController
@RequestMapping("/api/v1/requests/{id}")
@RequiredArgsConstructor
public class RequestController {
    private final RequestService service;

    /**
     * Ручка для получения заявки.
     */
    @GetMapping
    public ResponseEntity<?> read(
            @PathVariable(name = "id") long id
    ) {
        RequestDto body = service.read(id);
        return ResponseEntity.ok(body);
    }

    /**
     * Ручка для обновления заявки.
     */
    @PatchMapping
    public ResponseEntity<?> update(
            @PathVariable(name = "id") long id,
            @RequestBody @Valid RequestUpdatePayload payload
    ) {
        RequestDto body = service.update(id, payload);
        return ResponseEntity.ok(body);
    }

    /**
     * Ручка для удаления заявки.
     */
    @DeleteMapping
    public ResponseEntity<?> delete(
            @PathVariable(name = "id") long id
    ) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}