package com.supvz.requests_service.controller;

import com.supvz.requests_service.core.filter.RequestAssignmentFilter;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentPayload;
import com.supvz.requests_service.service.RequestAssignmentService;
import jakarta.annotation.Nullable;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * REST-контроллер для обработки ответов на заявки.
 */
@RestController
@RequestMapping("/api/v1/requests/assignments")
@RequiredArgsConstructor
public class RequestAssignmentsController {
    private final RequestAssignmentService service;

    /**
     * Ручка создания ответа на заявку.
     *
     * @param payload полезная нагрузка ответа на заявку.
     * @return {@link RequestAssignmentDto} - представление ответа на заявку для перемещения между слоями, приложениями.
     */
    @PostMapping
    public ResponseEntity<RequestAssignmentDto> create(
            @RequestBody @Valid RequestAssignmentPayload payload
    ) {
        RequestAssignmentDto body = service.create(payload);
        return ResponseEntity.ok(body);
    }

    /**
     * Ручка получения ответов мастеров по запросу.
     *
     * @param page номер страницы.
     * @param size размер выборки страницы.
     * @param filter фильтр для фильтрации ответов на заявку.
     * @return {@link PageDto} с {@link RequestAssignmentDto} - представление страницы и ответов на заявки для перемещения между слоями, приложениями.
     */
    @GetMapping
    public ResponseEntity<PageDto<RequestAssignmentDto>> readAll(
            @RequestParam(name = "page", defaultValue = "0") int page,
            @RequestParam(name = "size", defaultValue = "5") int size,
            @ModelAttribute @Nullable RequestAssignmentFilter filter
    ) {
        PageDto<RequestAssignmentDto> body = service.readAll(page, size, filter);
        return ResponseEntity.ok(body);
    }
}