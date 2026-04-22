package com.supvz.notifications_service.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.notifications_service.core.exception.NotificationNotFoundException;
import com.supvz.notifications_service.core.filter.NotificationFilter;
import com.supvz.notifications_service.model.dto.NotificationDto;
import com.supvz.notifications_service.model.dto.PageDto;
import com.supvz.notifications_service.model.entity.NotificationType;
import com.supvz.notifications_service.service.entity.NotificationService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;

import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;
import java.util.List;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(NotificationsController.class)
public class NotificationsControllerTests {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private NotificationService notificationService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void readAll_ShouldReturnPageOfNotifications() throws Exception {
        // given
        NotificationDto dto = NotificationDto.builder()
                .id(1L)
                .recipientId("user123")
                .body("Test body")
                .subject("Test subject")
                .sentAt(LocalDateTime.now())
                .viewed(false)
                .notificationType(NotificationType.email)
                .build();

        PageDto<NotificationDto> pageDto = new PageDto<>(
                List.of(dto),
                0,
                5,
                1,
                false,
                false
        );

        when(notificationService.findAll(eq(0), eq(5), any(NotificationFilter.class)))
                .thenReturn(pageDto);

        // when + then
        mockMvc.perform(get("/api/v1/notifications")
                        .param("page", "0")
                        .param("size", "5")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.content[0].id").value(1))
                .andExpect(jsonPath("$.page").value(0))
                .andExpect(jsonPath("$.total").value(1));
    }

    @Test
    void readAll_WithFilter_ShouldPassFilterToService() throws Exception {
        PageDto<NotificationDto> pageDto = new PageDto<>(List.of(), 0, 5, 0, false, false);
        when(notificationService.findAll(anyInt(), anyInt(), any(NotificationFilter.class)))
                .thenReturn(pageDto);

        mockMvc.perform(get("/api/v1/notifications")
                        .param("type", "web")
                        .param("recipientId", "user456"))
                .andExpect(status().isOk());

        verify(notificationService).findAll(eq(0), eq(5), argThat(f ->
                f.type() == NotificationType.web &&
                        "user456".equals(f.recipientId())
        ));
    }

    @Test
    void setNotificationViewed_ShouldCallServiceAndReturnOk() throws Exception {
        Long id = 123L;

        doNothing().when(notificationService).setViewed(eq(id));

        mockMvc.perform(patch("/api/v1/notifications/{id}", id))
                .andExpect(status().isOk());

        verify(notificationService).setViewed(id);
    }

    @Test
    void setNotificationViewed_WhenNotFound_ShouldReturn404() throws Exception {
        Long id = 999L;
        doThrow(new NotificationNotFoundException("Not found"))
                .when(notificationService).setViewed(id);

        mockMvc.perform(patch("/api/v1/notifications/{id}", id))
                .andExpect(status().isBadRequest());
    }
}