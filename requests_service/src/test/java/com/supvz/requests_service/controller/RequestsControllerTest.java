package com.supvz.requests_service.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jdk8.Jdk8Module;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.supvz.requests_service.core.PageDto;
import com.supvz.requests_service.core.RequestDto;
import com.supvz.requests_service.core.RequestPayload;
import com.supvz.requests_service.service.RequestService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.util.List;
import java.util.UUID;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(controllers = RequestsController.class)
@AutoConfigureMockMvc(addFilters = false)
class RequestsControllerTest {
    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockitoBean
    private RequestService service;

    private static final String URI = "/api/v1/requests";

    @BeforeEach
    void setup() {
        objectMapper.registerModule(new JavaTimeModule());
        objectMapper.registerModule(new Jdk8Module());
    }


    @Test
    void create__ValidPayload__ReturnsOk() throws Exception {
        UUID appellantId = UUID.randomUUID();
        RequestPayload payload = new RequestPayload(1, appellantId, null);
        RequestDto body = RequestDto.builder()
                .pvzId(1)
                .appellantId(appellantId)
                .description(null)
                .build();

        when(service.create(payload)).thenReturn(body);

        mvc.perform(post(URI)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(body)));

        verify(service, times(1)).create(payload);
    }

    @Test
    void create__InvalidPayload__ReturnsBadRequest() throws Exception {
        RequestPayload payload = new RequestPayload(1, null, null);

        mvc.perform(post(URI)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(service);
    }

    @Test
    void readAll__ReturnsOk() throws Exception {
        int page = 0;
        int size = 5;

        PageDto<RequestDto> body = new PageDto<>(List.of(), page, size, 1, false, false);

        when(service.readAll(page, size, null)).thenReturn(body);

        MvcResult result = mvc.perform(get(URI)
                        .param("page", String.valueOf(page))
                        .param("size", String.valueOf(size)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(body)))
                .andReturn();

        System.out.println("Response: " + result.getResponse().getContentAsString());

    }


}