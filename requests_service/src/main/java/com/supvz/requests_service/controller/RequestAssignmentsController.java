package com.supvz.requests_service.controller;

import com.supvz.requests_service.core.filter.RequestAssignmentFilter;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentPayload;
import com.supvz.requests_service.service.RequestAssignmentService;
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
 * REST-контроллер для обработки обращений на заявки.
 */
@RestController
@RequestMapping("/api/v1/requests/assignments")
@RequiredArgsConstructor
@Tag(name = "Request Assignments", description = "Управление обращениями на заявки: создание и просмотр списка")
public class RequestAssignmentsController {
    private final RequestAssignmentService service;

    /**
     * Ручка создания обращения на заявку.
     *
     * @param payload полезная нагрузка обращения на заявку.
     * @return {@link RequestAssignmentDto} - представление обращения на заявку для перемещения между слоями, приложениями.
     */
    @Operation(
            summary = "Создать новое обращение на заявку",
            description = "Создаёт новое обращение (например, от исполнителя или клиента) по существующей заявке. Возвращает полное представление созданного обращения."
    )
    @ApiResponse(
            responseCode = "200",
            description = "Обращение успешно создано",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = RequestAssignmentDto.class))
    )
    @ApiResponse(responseCode = "400", description = "Некорректные данные в payload (ошибки валидации)")
    @ApiResponse(responseCode = "404", description = "Заявка, на которую создаётся обращение, не найдена")
    @PostMapping
    public ResponseEntity<RequestAssignmentDto> create(
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    description = "Данные для создания обращения на заявку",
                    required = true,
                    content = @Content(schema = @Schema(implementation = RequestAssignmentPayload.class))
            )
            @RequestBody @Valid RequestAssignmentPayload payload
    ) {
        RequestAssignmentDto body = service.create(payload);
        return ResponseEntity.ok(body);
    }

    /**
     * Ручка получения обращений мастеров по заявке.
     *
     * @param page   номер страницы.
     * @param size   размер выборки страницы.
     * @param filter фильтр для фильтрации обращений на заявку.
     * @return {@link PageDto} с {@link RequestAssignmentDto} - представление страницы обращений на заявки для перемещения между слоями, приложениями.
     */
    @Operation(
            summary = "Получить список обращений на заявки с пагинацией и фильтрацией",
            description = "Возвращает страницу обращений с возможностью фильтрации по заявке, статусу, исполнителю, дате и другим критериям."
    )
    @ApiResponse(
            responseCode = "200",
            description = "Список обращений успешно получен",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = PageDto.class))
    )
    @GetMapping
    public ResponseEntity<PageDto<RequestAssignmentDto>> readAll(
            @Parameter(description = "Номер страницы (начинается с 0)", example = "0")
            @RequestParam(name = "page", defaultValue = "0") int page,
            @Parameter(description = "Размер страницы (рекомендуется ≤ 50)", example = "10")
            @RequestParam(name = "size", defaultValue = "5") int size,
            @Parameter(description = "Параметры фильтрации обращений")
            @ModelAttribute @Nullable RequestAssignmentFilter filter
    ) {
        PageDto<RequestAssignmentDto> body = service.readAll(page, size, filter);
        return ResponseEntity.ok(body);
    }
}