package com.supvz.requests_service.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.supvz.requests_service.core.*;
import com.supvz.requests_service.service.RequestAssignmentService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.UUID;

import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(controllers = RequestAssignmentController.class)
class RequestAssignmentControllerTest {
    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockitoBean
    private RequestAssignmentService service;

    private static final String URI = "/api/v1/requests/assignments/%s";

    @Test
    void read__ReturnsOk() throws Exception {
        int assignmentId = 1;

        RequestAssignmentDto body = RequestAssignmentDto.builder()
                .id(assignmentId)
                .build();

        when(service.read(assignmentId)).thenReturn(RequestAssignmentDto.builder()
                .id(assignmentId)
                .build());

        mvc.perform(get(URI.formatted(assignmentId)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(body)));

        verify(service, times(1)).read(assignmentId);
    }


    @Test
    void read__RequestAssignmentNotFound__ReturnsBadRequest() throws Exception {
        int assignmentId = 1;


        when(service.read(assignmentId))
                .thenThrow(new RequestAssignmentNotFoundException("test"));

        mvc.perform(get(URI.formatted(assignmentId)))
                .andExpect(status().isBadRequest());

        verify(service, times(1)).read(assignmentId);
    }

    @Test
    void update__ReturnsOk() throws Exception {
        int id = 1;

        Status status = Status.CONFIRMED;
        UUID handymanId = UUID.randomUUID();
        String newDescription = "test";
        RequestAssignmentUpdatePayload payload = new RequestAssignmentUpdatePayload(status, handymanId, newDescription);

        RequestAssignmentDto body = RequestAssignmentDto.builder()
                .id(id)
                .description(newDescription)
                .handymanId(handymanId)
                .status(status)
                .build();

        when(service.update(id, payload)).thenReturn(RequestAssignmentDto.builder()
                .id(id)
                .description(newDescription)
                .handymanId(handymanId)
                .status(status)
                .build());

        mvc.perform(patch(URI.formatted(id))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isOk())
                .andExpect(content().json(objectMapper.writeValueAsString(body)));

        verify(service, times(1)).update(id, payload);
    }

    @Test
    void update__RequestAssignmentNotFound__ReturnsBadRequest() throws Exception {
        int id = 1;

        Status status = Status.CONFIRMED;
        UUID handymanId = UUID.randomUUID();
        String newDescription = "test";
        RequestAssignmentUpdatePayload payload = new RequestAssignmentUpdatePayload(status, handymanId, newDescription);

        when(service.update(id, payload)).thenThrow(new RequestAssignmentNotFoundException("test"));

        mvc.perform(patch(URI.formatted(id))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isBadRequest());

        verify(service, times(1)).update(id, payload);
    }

    @Test
    void update__InvalidPayload__ReturnsBadRequest() throws Exception {
        int id = 1;

        RequestAssignmentUpdatePayload payload = new RequestAssignmentUpdatePayload(null, null, null);

        mvc.perform(patch(URI.formatted(id))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(payload)))
                .andExpect(status().isBadRequest());

        verifyNoInteractions(service);
    }

    @Test
    void delete__ReturnsNoContent() throws Exception {
        int id = 1;

        mvc.perform(delete(URI.formatted(id)))
                .andExpect(status().isNoContent());

        verify(service, times(1)).delete(id);
    }

    @Test
    void delete__RequestNotFound__ReturnsBadRequest() throws Exception {
        int id = 1;

        doThrow(new RequestAssignmentNotFoundException("test")).when(service).delete(id);

        mvc.perform(delete(URI.formatted(id)))
                .andExpect(status().isBadRequest());

        verify(service, times(1)).delete(id);
    }

}