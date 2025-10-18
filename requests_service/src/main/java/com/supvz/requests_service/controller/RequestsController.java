package com.supvz.requests_service.controller;

import com.supvz.requests_service.core.PageDto;
import com.supvz.requests_service.core.RequestDto;
import com.supvz.requests_service.core.RequestFilter;
import com.supvz.requests_service.core.RequestPayload;
import com.supvz.requests_service.service.RequestService;
import jakarta.annotation.Nullable;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/requests")
@RequiredArgsConstructor
/*
Контроллер для работы с запросами для мастеров.
 */
public class RequestsController {
    private final RequestService service;


    /*
    Ручка для создания запроса.
     */
    @PostMapping
    public ResponseEntity<?> create(
            @RequestBody @Valid RequestPayload payload
    ) {
        RequestDto body = service.create(payload);
        return ResponseEntity.ok(body);
    }


    /*
    Ручка для получения всех запросов с пагинацией.
    Параметр page для номера страницы.
    Параметр size для размера получаемой выборки.
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