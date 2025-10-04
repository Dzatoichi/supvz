package com.supvz.requests_service.service.impl;

import com.supvz.requests_service.core.*;
import com.supvz.requests_service.entity.Request;
import com.supvz.requests_service.mapper.RequestMapper;
import com.supvz.requests_service.repo.RequestRepository;
import com.supvz.requests_service.service.RequestService;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class RequestServiceImpl implements RequestService {
    private final RequestMapper mapper;
    private final RequestRepository repo;

    @Override
    public RequestDto create(RequestPayload payload) {
        log.info("CREATE REQUEST FOR PVZ [{}]. APPELLANT [{}].", payload.pvzId(), payload.appellantId());

        Request mapped = mapper.create(payload);

        Request saved = repo.save(mapped);

        log.info("REQUEST [{}] FOR PVZ [{}] IS CREATED. APPELLANT [{}].", saved.getId(), saved.getPvzId(), saved.getAppellantId());
        return mapper.read(saved);
    }

    @Override
    public PageDto<RequestDto> readAll(int pageNumber, int size, RequestFilter filter) {
        Integer pvzId = filter.pvzId();
        UUID appellantId = filter.appellantId();
        log.info("READ REQUEST PAGE. PVZ [{}], APPELLANT [{}], PAGE [{}], SIZE [{}].", pvzId == null ? "ANY" : pvzId, appellantId == null ? "ANY" : appellantId, pageNumber, size);

        Pageable pageable = PageRequest.of(pageNumber, size);

        Page<Request> page = repo.findAll(pvzId, appellantId, pageable);

        return mapper.readPage(page);
    }

    @Override
    public RequestDto read(long id) {
        log.info("READ REQUEST [{}].", id);

        return repo.findById(id)
                .map(mapper::read)
                .orElseThrow(() -> new RequestNotFoundException("REQUEST [%S] WAS NOT FOUND.".formatted(id)));
    }

    @Override
    public RequestDto update(long id, RequestUpdatePayload payload) {
        log.info("UPDATE REQUEST [{}].", id);

        Request found = repo.findById(id)
                .orElseThrow(() -> new RequestNotFoundException("REQUEST [%S] WAS NOT FOUND.".formatted(id)));

        Request mapped = mapper.update(found, payload);
        Request saved = repo.save(mapped);

        log.info("REQUEST [{}] IS UPDATED.", saved.getId());
        return mapper.read(saved);
    }

    @Override
    @Transactional
    public void delete(long id) {
        log.info("DELETE REQUEST [{}].", id);

        Request found = repo.findById(id)
                .orElseThrow(() -> new RequestNotFoundException("REQUEST [%S] WAS NOT FOUND.".formatted(id)));
        repo.delete(found);

        log.info("REQUEST [{}] IS DELETED.", id);
    }

    @Override
    public Request get(long id) {
        log.info("GET REQUEST [{}].", id);
        return repo.findById(id)
                .orElseThrow(() -> new RequestNotFoundException("REQUEST [%S] WAS NOT FOUND.".formatted(id)));
    }
}
