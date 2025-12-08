package com.supvz.requests_service.controller;

import com.supvz.requests_service.model.dto.RequestDto;
import com.supvz.requests_service.model.dto.RequestUpdatePayload;
import com.supvz.requests_service.service.RequestService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * REST-контроллер для обработки заявок.
 * Данный класс предназначен для работы с конкретными заявками по их идентификатору.
 */
@RestController
@RequestMapping("/api/v1/requests/{id}")
@RequiredArgsConstructor
public class RequestController {
    private final RequestService service;

    /**
     * Ручка для получения заявки по идентификатору.
     *
     * @param id идентификатор заявки.
     * @return {@link RequestDto} представление заявки для передачи между слоями, приложениями.
     */
    @GetMapping
    public ResponseEntity<RequestDto> read(
            @PathVariable(name = "id") long id
    ) {
        RequestDto body = service.read(id);
        return ResponseEntity.ok(body);
    }

    /**
     * Ручка для обновления заявки.
     *
     * @param id      идентификатор заявки
     * @param payload полезная нагрузка заявки
     * @return {@link RequestDto} представление заявки для передачи между слоями, приложениями.
     */
    @PatchMapping
    public ResponseEntity<RequestDto> update(
            @PathVariable(name = "id") long id,
            @RequestBody @Valid RequestUpdatePayload payload
    ) {
        RequestDto body = service.update(id, payload);
        return ResponseEntity.ok(body);
    }

    /**
     * Ручка для удаления заявки.
     *
     * @param id идентификатор заявки
     * @return {@link ResponseEntity} response ответ.
     */
    @DeleteMapping
    public ResponseEntity<?> delete(
            @PathVariable(name = "id") long id
    ) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}