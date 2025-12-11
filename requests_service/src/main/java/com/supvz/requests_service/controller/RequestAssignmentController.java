package com.supvz.requests_service.controller;

import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.service.RequestAssignmentService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * REST-контроллер для обработки обращений на заявки.
 * Данный класс предназначен для работы с конкретными обращениями на заявки по их идентификатору.
 */
@RestController
@RequestMapping("/api/v1/requests/assignments/{id}")
@RequiredArgsConstructor
public class RequestAssignmentController {
    private final RequestAssignmentService service;

    /**
     * Ручка для получения обращения на заявку.
     *
     * @param id идентификатор обращения на заявку.
     * @return {@link RequestAssignmentDto} - представление обращения на заявку для перемещения между слоями, приложениями.
     */
    @GetMapping
    public ResponseEntity<RequestAssignmentDto> read(
            @PathVariable(name = "id") long id
    ) {
        RequestAssignmentDto body = service.read(id);
        return ResponseEntity.ok(body);
    }

    /**
     * Ручка для обновления обращения на заявку.
     *
     * @param id      идентификатор обращения на заявку.
     * @param payload полезная нагрузка для обновления обращения на заявку.
     * @return {@link RequestAssignmentDto} - представление обращения на заявку для перемещения между слоями, приложениями.
     */
    @PatchMapping
    public ResponseEntity<RequestAssignmentDto> update(
            @PathVariable(name = "id") long id,
            @RequestBody @Valid RequestAssignmentUpdatePayload payload
    ) {
        RequestAssignmentDto body = service.update(id, payload);
        return ResponseEntity.ok(body);
    }
}