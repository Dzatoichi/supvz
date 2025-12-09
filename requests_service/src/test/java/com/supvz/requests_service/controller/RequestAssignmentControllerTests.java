package com.supvz.requests_service.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.requests_service.core.exception.RequestAssignmentNotFoundException;
import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.service.RequestAssignmentService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(controllers = RequestAssignmentController.class)
class RequestAssignmentControllerTests {
    @Autowired
    private MockMvc mvc;
    @Autowired
    private ObjectMapper objectMapper;
    @MockitoBean
    private RequestAssignmentService service;
    private static final String URI = "/api/v1/requests/assignments/%s";

    @Test
    void read__ReturnsOk() throws Exception {
        int assignmentIdMock = 1;
        RequestAssignmentDto dtoMock = new RequestAssignmentDto(1, 1, 1, null, null, null, null, null);

        when(service.read(assignmentIdMock)).thenReturn(dtoMock);

        mvc.perform(get(URI.formatted(assignmentIdMock)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(dtoMock)));

        verify(service, times(1)).read(assignmentIdMock);
    }


    @Test
    void read__RequestAssignmentNotFound__ReturnsBadRequest() throws Exception {
        int assignmentIdMock = 1;

        when(service.read(assignmentIdMock))
                .thenThrow(new RequestAssignmentNotFoundException("messageMock"));

        mvc.perform(get(URI.formatted(assignmentIdMock)))
                .andExpect(status().isBadRequest());

        verify(service, times(1)).read(assignmentIdMock);
    }

    @Test
    void update__ReturnsOk() throws Exception {
        int assignmentIdMock = 1;

        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(null, null, null);
        RequestAssignmentDto dtoMock = new RequestAssignmentDto(1, 1, 1, null, null, null, null, null);

        when(service.update(assignmentIdMock, payloadMock)).thenReturn(dtoMock);

        mvc.perform(patch(URI.formatted(assignmentIdMock))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payloadMock)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(dtoMock)));

        verify(service, times(1)).update(assignmentIdMock, payloadMock);
    }

    @Test
    void update__RequestAssignmentNotFound__ReturnsBadRequest() throws Exception {
        int assignmentIdMock = 1;

        RequestAssignmentUpdatePayload payloadMock = new RequestAssignmentUpdatePayload(null, null, null);

        when(service.update(assignmentIdMock, payloadMock)).thenThrow(new RequestAssignmentNotFoundException("test"));

        mvc.perform(patch(URI.formatted(assignmentIdMock))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payloadMock)))
                .andExpect(status().isBadRequest());

        verify(service, times(1)).update(assignmentIdMock, payloadMock);
    }

    @Test
    void update__InvalidPayloadComment__ReturnsBadRequest() throws Exception {
        int assignmentIdMock = 1;

        RequestAssignmentUpdatePayload payload = new RequestAssignmentUpdatePayload(null, null, "  ");

        mvc.perform(patch(URI.formatted(assignmentIdMock))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(service);
    }
}