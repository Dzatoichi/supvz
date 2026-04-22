package com.supvz.requests_service.controller;

import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestDto;
import com.supvz.requests_service.core.filter.RequestFilter;
import com.supvz.requests_service.model.dto.RequestPayload;
import com.supvz.requests_service.model.dto.RequestPlainDto;
import com.supvz.requests_service.service.RequestService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
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
@Tag(name = "Requests", description = "Управление заявками: создание, просмотр списка с фильтрацией")
public class RequestsController {
    private final RequestService service;


    /**
     * Ручка создания заявки.
     *
     * @param payload полезная нагрузка для создания заявки.
     * @return {@link RequestDto} - представление заявки для передачи между слоями, приложениями.
     */
    @Operation(
            summary = "Создать новую заявку",
            description = "Создаёт новую заявку на основе переданных данных. Возвращает полное представление созданной заявки."
    )
    @ApiResponse(
            responseCode = "200",
            description = "Заявка успешно создана",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = RequestDto.class))
    )
    @ApiResponse(responseCode = "400", description = "Некорректные данные в payload (ошибки валидации)")
    @PostMapping
    public ResponseEntity<RequestDto> create(
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    description = "Данные для создания заявки",
                    required = true,
                    content = @Content(schema = @Schema(implementation = RequestPayload.class))
            )
            @RequestBody @Valid RequestPayload payload
    ) {
        RequestDto body = service.create(payload);
        return ResponseEntity.ok(body);
    }


    /**
     * Ручка для получения всех заявок с пагинацией.
     *
     * @param page   номер страницы.
     * @param size   размер получаемой выборки.
     * @param filter фильтр для фильтрации заявок.
     * @return {@link PageDto} с {@link RequestPlainDto} - представление страницы и заявок для передачи между слоями, приложениями.
     */
    @Operation(
            summary = "Получить список заявок с пагинацией и фильтрацией",
            description = "Возвращает страницу заявок с возможностью фильтрации по статусу, автору, дате и другим полям."
    )
    @ApiResponse(
            responseCode = "200",
            description = "Список заявок успешно получен",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = PageDto.class))
    )
    @GetMapping
    public ResponseEntity<PageDto<RequestPlainDto>> readAll(
            @Parameter(description = "Номер страницы (начинается с 0)", example = "0")
            @RequestParam(name = "page", defaultValue = "0") int page,
            @Parameter(description = "Размер страницы (рекомендуется ≤ 50)", example = "10")
            @RequestParam(name = "size", defaultValue = "5") int size,
            @Parameter(description = "Параметры фильтрации заявок")
            @ModelAttribute @Nullable RequestFilter filter
    ) {
        PageDto<RequestPlainDto> body = service.readAll(page, size, filter);
        return ResponseEntity.ok(body);
    }
}