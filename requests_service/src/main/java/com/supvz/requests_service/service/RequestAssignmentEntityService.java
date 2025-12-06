package com.supvz.requests_service.service.impl;

import com.supvz.requests_service.core.*;
import com.supvz.requests_service.entity.Request;
import com.supvz.requests_service.entity.RequestAssignment;
import com.supvz.requests_service.mapper.RequestAssignmentMapper;
import com.supvz.requests_service.repo.RequestAssignmentRepository;
import com.supvz.requests_service.service.RequestAssignmentService;
import com.supvz.requests_service.service.RequestService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
/*
Реализация сервиса для работы с ответами на запросы.
 */
public class RequestAssignmentServiceImpl implements RequestAssignmentService {
    private final RequestAssignmentMapper mapper;
    private final RequestAssignmentRepository repo;
    private final RequestService requestService;

    @Override
    @Transactional
    /*
    Метод для создания ответа-сущности по полученной нагрузке.
     */
    public RequestAssignmentDto create(long requestId, RequestAssignmentPayload payload) {
        log.info("CREATE REQUEST [{}] ASSIGNMENT BY HANDYMAN [{}].", requestId, payload.handymanId());

        Request request = requestService.get(requestId);
        RequestAssignment mapped = mapper.create(request, payload);

        RequestAssignment saved = repo.save(mapped);

        log.info("REQUEST ASSIGNMENT [{}] IS CREATED BY HANDYMAN [{}].", saved.getRequest().getId(), saved.getHandymanId());
        return mapper.read(saved);
    }

    @Override
    /*
    Метод для чтения страницы ответов на запрос с пагинацией.
     */
    public PageDto<RequestAssignmentDto> readAll(long requestId, int pageNumber, int size) {
        log.info("READ REQUEST [{}] ASSIGNMENTS PAGE. PAGE [{}], SIZE [{}].", requestId, pageNumber, size);

        Pageable pageable = PageRequest.of(pageNumber, size);
        Page<RequestAssignment> page = repo.findAll(requestId, pageable);

        return mapper.readPage(page);
    }

    @Override
    /*
    Метод для чтения определенного ответа на запрос по ID.
     */
    public RequestAssignmentDto read(long id) {
        log.info("READ REQUEST ASSIGNMENT [{}].", id);

        return repo.findById(id)
                .map(mapper::read)
                .orElseThrow(() -> new RequestAssignmentNotFoundException
                        ("REQUEST ASSIGNMENT [%s] WAS NOT FOUND.".formatted(id)));
    }

    @Override
    /*
    Метод для обновления определенного ответа на запрос по ID с полезной нагрузкой.
     */
    public RequestAssignmentDto update(long id, RequestAssignmentUpdatePayload payload) {
        log.info("UPDATE REQUEST ASSIGNMENT [{}]. Payload [{}].", id, payload);

        RequestAssignment found = repo.findById(id)
                .orElseThrow(() -> new RequestAssignmentNotFoundException
                        ("REQUEST ASSIGNMENT [%s] WAS NOT FOUND.".formatted(id)));

        RequestAssignment mapped = mapper.update(found, payload);
        RequestAssignment saved = repo.save(mapped);

        log.info("REQUEST ASSIGNMENT [{}] IS UPDATED.", saved.getId());
        return mapper.read(saved);
    }

    @Override
    @Transactional
    /*
    Метод для удаления определенного ответа на запрос по ID.
     */
    public void delete(long id) {
        log.info("DELETE REQUEST ASSIGNMENT [{}].", id);

        RequestAssignment found = repo.findById(id)
                .orElseThrow(() -> new RequestAssignmentNotFoundException
                        ("REQUEST ASSIGNMENT [%s] WAS NOT FOUND.".formatted(id)));
        repo.delete(found);

        log.info("REQUEST ASSIGNMENT [{}] IS DELETED.", id);
    }
}
