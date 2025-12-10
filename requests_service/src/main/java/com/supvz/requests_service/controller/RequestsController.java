package com.supvz.requests_service.controller;

import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestDto;
import com.supvz.requests_service.core.filter.RequestFilter;
import com.supvz.requests_service.model.dto.RequestPayload;
import com.supvz.requests_service.model.dto.RequestPlainDto;
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
     * Ручка создания заявки.
     *
     * @param payload полезная нагрузка для создания заявки.
     * @return {@link RequestDto} - представление заявки для передачи между слоями, приложениями.
     */
    @PostMapping
    public ResponseEntity<RequestDto> create(
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
     * @param filter фильтр для фильтрации заявок.
     * @return {@link PageDto} с {@link RequestPlainDto} - представление страницы и заявок для передачи между слоями, приложениями.
     */
    @GetMapping
    public ResponseEntity<PageDto<RequestPlainDto>> readAll(
            @RequestParam(name = "page", defaultValue = "0") int page,
            @RequestParam(name = "size", defaultValue = "5") int size,
            @ModelAttribute @Nullable RequestFilter filter
    ) {
        PageDto<RequestPlainDto> body = service.readAll(page, size, filter);
        return ResponseEntity.ok(body);
    }
}