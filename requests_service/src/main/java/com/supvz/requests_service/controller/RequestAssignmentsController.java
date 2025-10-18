package com.supvz.requests_service.controller;

import com.supvz.requests_service.core.PageDto;
import com.supvz.requests_service.core.RequestAssignmentDto;
import com.supvz.requests_service.core.RequestAssignmentPayload;
import com.supvz.requests_service.service.RequestAssignmentService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/requests/{id}/assignments")
@RequiredArgsConstructor
/*
Контроллер для работы с ответами мастеров на запросы.
 */
public class RequestAssignmentsController {
    private final RequestAssignmentService service;

    /*
    Ручка создания ответа мастера на запрос.
     */
    @PostMapping
    public ResponseEntity<?> create(
            @PathVariable(name = "id") long requestId,
            @RequestBody @Valid RequestAssignmentPayload payload
    ) {
        RequestAssignmentDto body = service.create(requestId, payload);
        return ResponseEntity.ok(body);
    }

    /*
    Ручка получения ответов мастеров по запросу.
     */
    @GetMapping
    public ResponseEntity<?> readAll (
            @RequestParam(name = "page", defaultValue = "0") int page,
            @RequestParam(name = "size", defaultValue = "5") int size,
            @PathVariable(name = "id") long requestId
    ) {
        PageDto<RequestAssignmentDto> body = service.readAll(requestId, page, size);
        return ResponseEntity.ok(body);
    }
}
