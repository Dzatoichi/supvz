package com.supvz.requests_service.controller;

import com.supvz.requests_service.model.dto.RequestDto;
import com.supvz.requests_service.model.dto.RequestUpdatePayload;
import com.supvz.requests_service.service.RequestService;
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
 * REST-контроллер для обработки заявок.
 * Данный класс предназначен для работы с конкретными заявками по их идентификатору.
 */
@RestController
@RequestMapping("/api/v1/requests/{id}")
@RequiredArgsConstructor
@Tag(name = "Requests", description = "Управление заявками: получение, обновление, удаление по ID")
public class RequestController {
    private final RequestService service;

    /**
     * Ручка для получения заявки по идентификатору.
     *
     * @param id идентификатор заявки.
     * @return {@link RequestDto} представление заявки для передачи между слоями, приложениями.
     */
    @Operation(
            summary = "Получить заявку по ID",
            description = "Возвращает полное представление заявки, включая все связанные данные (обращения, комментарии и т.д.)."
    )
    @ApiResponse(
            responseCode = "200",
            description = "Заявка найдена",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = RequestDto.class))
    )
    @ApiResponse(responseCode = "404", description = "Заявка с указанным ID не найдена")
    @GetMapping
    public ResponseEntity<RequestDto> read(
            @Parameter(description = "Уникальный идентификатор заявки", required = true, example = "123")
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
    @Operation(
            summary = "Частично обновить заявку",
            description = "Обновляет только указанные поля заявки (например, статус или приоритет). Используется PATCH-семантика."
    )
    @ApiResponse(
            responseCode = "200",
            description = "Заявка успешно обновлена",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = RequestDto.class))
    )
    @ApiResponse(responseCode = "400", description = "Ошибки валидации в payload")
    @ApiResponse(responseCode = "404", description = "Заявка не найдена")
    @PatchMapping
    public ResponseEntity<RequestDto> update(
            @Parameter(description = "Уникальный идентификатор заявки", required = true, example = "123")
            @PathVariable(name = "id") long id,
            @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    description = "Поля для обновления",
                    required = true,
                    content = @Content(schema = @Schema(implementation = RequestUpdatePayload.class))
            )
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
    @Operation(
            summary = "Удалить заявку",
            description = "Полностью удаляет заявку и все связанные с ней обращения (если разрешено бизнес-логикой)."
    )
    @ApiResponse(responseCode = "204", description = "Заявка успешно удалена")
    @ApiResponse(responseCode = "404", description = "Заявка не найдена")
    @DeleteMapping
    public ResponseEntity<?> delete(
            @Parameter(description = "Уникальный идентификатор заявки", required = true, example = "123")
            @PathVariable(name = "id") long id
    ) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}