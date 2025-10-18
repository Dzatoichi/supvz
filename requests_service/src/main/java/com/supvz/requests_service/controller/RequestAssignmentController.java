package com.supvz.requests_service.controller;

import com.supvz.requests_service.core.RequestAssignmentDto;
import com.supvz.requests_service.core.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.service.RequestAssignmentService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/requests/assignments/{id}")
@RequiredArgsConstructor
/*
Контроллер для работы с ответом мастера на запрос.
 */
public class RequestAssignmentController {
    private final RequestAssignmentService service;

    /*
    Ручка для получения ответа мастера.
     */
    @GetMapping
    public ResponseEntity<?> read(
            @PathVariable(name = "id") long id
    ) {
         RequestAssignmentDto body = service.read(id);
         return ResponseEntity.ok(body);
    }

    /*
    Ручка для обновления ответа мастера.
     */
    @PatchMapping
    public ResponseEntity<?> update(
            @PathVariable(name = "id") long id,
            @RequestBody @Valid RequestAssignmentUpdatePayload payload
            ) {
        RequestAssignmentDto body = service.update(id, payload);
        return ResponseEntity.ok(body);
    }

    /*
    Ручка для удаления ответа мастера.
     */
    @DeleteMapping
    public ResponseEntity<?> delete(
            @PathVariable(name = "id") long id
    ) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
