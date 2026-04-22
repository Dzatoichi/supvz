package com.supvz.notifications_service.controller;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.service.entity.NotificationService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.annotation.Nullable;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * <h3>
 * Контроллер для работы с нотификациями.
 * </h3>
 */
@RestController
@RequestMapping("/api/v1/notifications")
@RequiredArgsConstructor
@Tag(name = "Notifications", description = "Управление уведомлениями пользователей")
public class NotificationsController {
    private final NotificationService service;

    /**
     * Ручка для получения страницы с нотификациями с фильтрацией.
     *
     * @param page   номер страницы.
     * @param size   кол-во нотификаций в странице.
     * @param filter ДТО фильтра.
     * @return {@code ResponseEntity} - ответ от сервера со страницей нотификаций.
     */
    @Operation(
            summary = "Получить список уведомлений с пагинацией и фильтрацией",
            description = "Возвращает страницу уведомлений с возможностью фильтрации по типу, получателю и другим полям."
    )
    @ApiResponse(
            responseCode = "200",
            description = "Успешно получена страница уведомлений",
            content = @Content(mediaType = "application/json", schema = @Schema(implementation = PageDto.class))
    )
    @GetMapping
    public ResponseEntity<PageDto<NotificationDto>> readAll(
            @RequestParam(name = "page", defaultValue = "0", required = false) int page,
            @RequestParam(name = "size", defaultValue = "5", required = false) int size,
            @ModelAttribute @Nullable NotificationFilter filter
    ) {
        PageDto<NotificationDto> body = service.findAll(page, size, filter);
        return ResponseEntity.ok(body);
    }

    /**
     * Ручка для изменения статуса "Просмотрено" у нотификации.
     *
     * @param notificationId идентификатор нотификации.
     * @return {@code ResponseEntity} - ответ от сервера.
     */
    @Operation(
            summary = "Отметить уведомление как просмотренное",
            description = "Обновляет статус уведомления с указанным ID, устанавливая флаг 'viewed' в true."
    )
    @ApiResponse(responseCode = "200", description = "Уведомление успешно отмечено как просмотренное")
    @ApiResponse(responseCode = "404", description = "Уведомление с указанным ID не найдено")
    @PatchMapping("/{id}")
    public ResponseEntity<?> setNotificationViewed(
            @PathVariable(name = "id") Long notificationId
    ) {
        service.setViewed(notificationId);
        return ResponseEntity.ok().build();
    }
}