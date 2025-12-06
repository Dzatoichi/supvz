package com.supvz.requests_service.service;

import com.supvz.requests_service.core.exception.RequestNotFoundException;
import com.supvz.requests_service.core.filter.RequestFilter;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestDto;
import com.supvz.requests_service.model.dto.RequestPayload;
import com.supvz.requests_service.model.dto.RequestUpdatePayload;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.mapper.RequestMapper;
import com.supvz.requests_service.repo.RequestRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.UUID;

/**
 * Реализация сервиса для обработки заявок.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class RequestEntityService implements RequestService {
    private final RequestMapper mapper;
    private final RequestRepository repo;

    /**
     * Метод для создания сущности заявки.
     */
    @Override
    public RequestDto create(RequestPayload payload) {
        log.debug("Создание заявки по ПВЗ [{}]. Подал: [{}].", payload.pvzId(), payload.appellantId());
        Request mapped = mapper.create(payload);
        Request saved = repo.save(mapped);
        log.info("Заявка [{}] по ПВЗ [{}] успешно создана. Подал: [{}].", saved.getId(), saved.getPvzId(), saved.getAppellantId());
        return mapper.read(saved);
    }
//    todo: конфликт

    /**
     * Метод для чтения страницы заявок с пагинацией и фильтрацией.
     */
    @Override
    public PageDto<RequestDto> readAll(int pageNumber, int size, RequestFilter filter) {
        Integer pvzId = filter.pvzId();
        Long appellantId = filter.appellantId();
        Pageable pageable = PageRequest.of(pageNumber, size);
        Page<Request> page = repo.findAll(pvzId, appellantId, pageable);
        return mapper.readPage(page);
    }
//    TODO: использовать спецификации

    /**
     * Метод для чтения определенной заявки по ID.
     */
    @Override
    public RequestDto read(long id) {
        log.debug("Получение заявки [{}].", id);
        return repo.findById(id)
                .map(mapper::read)
                .orElseThrow(() -> new RequestNotFoundException("Заявка [%S] не найдена.".formatted(id)));
    }

    /**
     * Метод для обновления определенной заявки по ID с полезной нагрузкой.
     */
    @Override
    public RequestDto update(long id, RequestUpdatePayload payload) {
        log.debug("Обновление заявки [{}].", id);
        Request found = repo.findById(id)
                .orElseThrow(() -> new RequestNotFoundException("Заявка [%S] не найдена.".formatted(id)));
        Request mapped = mapper.update(found, payload);
        Request saved = repo.save(mapped);
        log.info("Заявка [{}] успешно обновлена.", saved.getId());
        return mapper.read(saved);
    }

    /**
     * Метод для удаления определенной заявки по ID.
     */
    @Override
    @Transactional
    public void delete(long id) {
        log.debug("Удаление заявки [{}].", id);
        Request found = repo.findById(id)
                .orElseThrow(() -> new RequestNotFoundException("Заявка [%S] не найдена.".formatted(id)));
        repo.delete(found);
        log.info("Заявка [{}] успешно удалена.", id);
    }

    /**
     * Метод для получения определенной заявки по ID.
     */
    @Override
    public Request get(long id) {
        log.debug("Получение сущности заявки [{}].", id);
        return repo.findById(id)
                .orElseThrow(() -> new RequestNotFoundException("Заявка [%S] не найдена.".formatted(id)));
    }
}
// TODO: логи исправить и перевести