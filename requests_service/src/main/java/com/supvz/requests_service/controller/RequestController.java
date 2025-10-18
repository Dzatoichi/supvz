package com.supvz.requests_service.controller;

import com.supvz.requests_service.core.RequestDto;
import com.supvz.requests_service.core.RequestUpdatePayload;
import com.supvz.requests_service.service.RequestService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/requests/{id}")
@RequiredArgsConstructor
/*
Контроллер для работы с запросом для мастера.
 */
public class RequestController {
    private final RequestService service;

    /*
    Ручка для получения запроса.
     */
    @GetMapping
    public ResponseEntity<?> read(
            @PathVariable(name = "id") long id
    ) {
        RequestDto body = service.read(id);
        return ResponseEntity.ok(body);
    }

    /*
    Ручка для обновления запроса.
     */
    @PatchMapping
    public ResponseEntity<?> update(
            @PathVariable(name = "id") long id,
            @RequestBody @Valid RequestUpdatePayload payload
    ) {
        RequestDto body = service.update(id, payload);
        return ResponseEntity.ok(body);
    }

    /*
    Ручка для удаления запроса.
     */
    @DeleteMapping
    public ResponseEntity<?> delete(
            @PathVariable(name = "id") long id
    ) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
