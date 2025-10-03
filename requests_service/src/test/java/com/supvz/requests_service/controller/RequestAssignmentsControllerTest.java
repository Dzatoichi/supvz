package com.supvz.requests_service.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.requests_service.core.PageDto;
import com.supvz.requests_service.core.RequestAssignmentDto;
import com.supvz.requests_service.core.RequestAssignmentPayload;
import com.supvz.requests_service.service.RequestAssignmentService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;
import java.util.UUID;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(controllers = RequestAssignmentsController.class)
class RequestAssignmentsControllerTest {
    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockitoBean
    private RequestAssignmentService service;

    private static final String URI = "/api/v1/requests/%s/assignments";

    @Test
    void create__ValidPayload__ReturnsOk() throws Exception {
        int requestId = 1;
        UUID handymanId = UUID.randomUUID();
        RequestAssignmentPayload payload = new RequestAssignmentPayload(handymanId, null);

        RequestAssignmentDto body = RequestAssignmentDto.builder()
                .requestId(requestId)
                .handymanId(handymanId)
                .build();

        when(service.create(requestId, payload))
                .thenReturn(RequestAssignmentDto.builder()
                        .requestId(requestId)
                        .handymanId(handymanId)
                        .build());

        mvc.perform(post(URI.formatted(requestId))
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(body)));

        verify(service, times(1)).create(requestId, payload);

    }


    @Test
    void create__InvalidPayload__ReturnsBadRequest() throws Exception {
        int requestId = 1;
        RequestAssignmentPayload payload = new RequestAssignmentPayload(null, null);

        mvc.perform(post(URI.formatted(requestId))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(service);
    }

    @Test
    void readAll__ReturnsOk() throws Exception {
        int requestId = 1;
        int page = 0;
        int size = 5;

        PageDto<RequestAssignmentDto> body = PageDto.<RequestAssignmentDto>builder()
                .content(List.of())
                .page(page)
                .size(size)
                .total(0)
                .hasNext(false)
                .hasPrev(false)
                .build();

        when(service.readAll(requestId, page, size)).thenReturn(PageDto.<RequestAssignmentDto>builder()
                .content(List.of())
                .page(page)
                .size(size)
                .total(0)
                .hasNext(false)
                .hasPrev(false)
                .build());

        mvc.perform(get(URI.formatted(requestId))
                        .param("page", String.valueOf(page))
                        .param("size", String.valueOf(size)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(body)));

        verify(service, times(1)).readAll(requestId, page, size);
    }

}