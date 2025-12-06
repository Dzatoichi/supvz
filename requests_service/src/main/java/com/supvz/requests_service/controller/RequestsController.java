package com.supvz.requests_service.controller;

import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestDto;
import com.supvz.requests_service.core.filter.RequestFilter;
import com.supvz.requests_service.model.dto.RequestPayload;
import com.supvz.requests_service.service.RequestService;
import jakarta.annotation.Nullable;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


/**
 * REST-контроллер для обработки заявок.
 */
@RestController
@RequestMapping("/api/v1/requests")
@RequiredArgsConstructor
public class RequestsController {
    private final RequestService service;


    /**
     * Ручка для создания заявки.
     */
    @PostMapping
    public ResponseEntity<?> create(
            @RequestBody @Valid RequestPayload payload
    ) {
        RequestDto body = service.create(payload);
        return ResponseEntity.ok(body);
    }


    /**
     * Ручка для получения всех заявок с пагинацией.
     *
     * @param page номер страницы.
     * @param size размер получаемой выборки.
     */
    @GetMapping
    public ResponseEntity<?> readAll(
            @RequestParam(name = "page", defaultValue = "0") int page,
            @RequestParam(name = "size", defaultValue = "5") int size,
            @ModelAttribute @Nullable RequestFilter filter
    ) {
        PageDto<RequestDto> body = service.readAll(page, size, filter);
        return ResponseEntity.ok(body);
    }
}