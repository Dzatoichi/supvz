package com.supvz.requests_service.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestDto;
import com.supvz.requests_service.core.filter.RequestFilter;
import com.supvz.requests_service.model.dto.RequestPayload;
import com.supvz.requests_service.model.dto.RequestPlainDto;
import com.supvz.requests_service.service.RequestService;
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

@WebMvcTest(controllers = RequestsController.class)
class RequestsControllerTests {
    @Autowired
    private MockMvc mvc;
    @Autowired
    private ObjectMapper objectMapper;
    @MockitoBean
    private RequestService service;
    private static final String URI = "/api/v1/requests";

    @Test
    void create__ValidPayload__ReturnsOk() throws Exception {
        RequestPayload payloadMock = new RequestPayload(1, 1, null, null);
        RequestDto dtoMock = new RequestDto(1, 1, 1, null, null, null, null);

        when(service.create(payloadMock)).thenReturn(dtoMock);

        mvc.perform(post(URI)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payloadMock)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(dtoMock)));

        verify(service, times(1)).create(payloadMock);
    }

    @Test
    void create__InvalidPayloadSubject__ReturnsBadRequest() throws Exception {
        RequestPayload payloadMock = new RequestPayload(1, 1, "  ", null);
        mvc.perform(post(URI)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payloadMock)))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(service);
    }

    @Test
    void create__InvalidPayloadDescription__ReturnsBadRequest() throws Exception {
        RequestPayload payloadMock = new RequestPayload(1, 1, null, "   ");
        mvc.perform(post(URI)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payloadMock)))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(service);
    }

    @Test
    void readAll__ReturnsOk() throws Exception {
        int page = 0;
        int size = 5;
        RequestFilter filter = new RequestFilter(null, null, null, null);

        PageDto<RequestPlainDto> body = new PageDto<>(List.of(), page, size, 1, false, false);

        when(service.readAll(page, size, filter))
                .thenReturn(new PageDto<>(List.of(), page, size, 1, false, false));

        mvc.perform(get(URI)
                        .param("page", String.valueOf(page))
                        .param("size", String.valueOf(size)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(body)));


        verify(service, times(1)).readAll(page, size, filter);
    }
}