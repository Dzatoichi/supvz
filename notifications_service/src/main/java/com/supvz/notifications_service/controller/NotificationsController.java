package com.supvz.notifications_service.controller;

import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.service.entity.NotificationService;
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
@RequestMapping(name = "/api/v1/notifications")
@RequiredArgsConstructor
public class NotificationsController {
    private final NotificationService service;

    /**
     * Ручка для получения страницы с нотификациями с фильтрацией.
     * @param page номер страницы.
     * @param size кол-во нотификаций в странице.
     * @param filter ДТО фильтра.
     * @return ResponseEntity - ответ от сервера со страницей нотификаций.
     */
    @GetMapping
    public ResponseEntity<PageDto<NotificationDto>> readAll(
            @RequestParam(name = "page", defaultValue = "0", required = false) int page,
            @RequestParam(name = "size", defaultValue = "5", required = false) int size,
            @ModelAttribute @Nullable NotificationFilter filter
    ) {
        PageDto<NotificationDto> body = service.findAll(page, size, filter);
        return ResponseEntity.ok(body);
    }
}
