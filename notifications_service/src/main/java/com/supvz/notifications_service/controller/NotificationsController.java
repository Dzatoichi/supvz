package com.supvz.notifications_service.controller;

import com.supvz.notifications_service.core.dto.NotificationDto;
import com.supvz.notifications_service.core.dto.PageDto;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.service.NotificationService;
import jakarta.annotation.Nullable;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping(name = "/api/v1/notifications")
@RequiredArgsConstructor
public class NotificationsController {
    private final NotificationService service;

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
