package com.supvz.requests_service.controller;

import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.service.RequestAssignmentService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
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
@Tag(name = "Request Assignments", description = "Операции с конкретными обращениями на заявки по их ID")
public class RequestAssignmentController {
    private final RequestAssignmentService service;

    /**
     * Ручка для получения обращения на заявку.
     *
     * @param id идентификатор обращения на заявку.
     * @return {@link RequestAssignmentDto} - представление обращения на заявку для перемещения между слоями, приложениями.
     */
    @Operation(
            summary = "Получить обращение на заявку по ID",
            description = "Возвращает полное представление обращения на заявку, включая статус, исполнителя, комментарии и связанные данные."
    )
    @ApiResponse(
            responseCode = "200",
            description = "Обращение успешно найдено",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = RequestAssignmentDto.class))
    )
    @ApiResponse(responseCode = "404", description = "Обращение с указанным ID не найдено")
    @GetMapping
    public ResponseEntity<RequestAssignmentDto> read(
            @Parameter(description = "Уникальный идентификатор обращения на заявку", required = true, example = "123")
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
    @Operation(
            summary = "Частично обновить обращение на заявку",
            description = "Обновляет только указанные поля обращения (например, статус или комментарий). Используется PATCH-семантика."
    )
    @ApiResponse(
            responseCode = "200",
            description = "Обращение успешно обновлено",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = RequestAssignmentDto.class))
    )
    @ApiResponse(responseCode = "400", description = "Некорректные данные в запросе (валидация payload)")
    @ApiResponse(responseCode = "404", description = "Обращение с указанным ID не найдено")
    @PatchMapping
    public ResponseEntity<RequestAssignmentDto> update(
            @Parameter(description = "Уникальный идентификатор обращения на заявку", required = true, example = "123")
            @PathVariable(name = "id") long id,
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    description = "Данные для обновления обращения",
                    required = true,
                    content = @Content(schema = @Schema(implementation = RequestAssignmentUpdatePayload.class))
            )
            @RequestBody @Valid RequestAssignmentUpdatePayload payload
    ) {
        RequestAssignmentDto body = service.update(id, payload);
        return ResponseEntity.ok(body);
    }
}