package com.supvz.requests_service.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentPayload;
import com.supvz.requests_service.service.RequestAssignmentService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

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
        RequestAssignmentPayload payloadMock = new RequestAssignmentPayload(1, null);
        RequestAssignmentDto dtoMock = new RequestAssignmentDto(1, 1, 1, null, null, null, null, null);

        when(service.create(1, payloadMock)).thenReturn(dtoMock);

        mvc.perform(post(URI.formatted(1))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payloadMock)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(dtoMock)));

        verify(service, times(1)).create(1, payloadMock);
    }

    @Test
    void create__InvalidPayload__ReturnsBadRequest() throws Exception {
        int requestId = 1;
        RequestAssignmentPayload payload = new RequestAssignmentPayload(1, null);

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