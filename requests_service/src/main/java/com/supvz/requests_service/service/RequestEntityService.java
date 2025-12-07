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
import com.supvz.requests_service.util.specification.RequestSpecifications;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;

import java.util.UUID;

/**
 * Реализация сервиса для обработки заявок.
 * Отвечает за бизнес-логику заявок. Слой, что работает с сущностями напрямую.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class RequestEntityService implements RequestService {
    private final RequestMapper mapper;
    private final RequestRepository repo;

    /**
     * Создание сущности заявки.
     *
     * @param payload полезная нагрузка для создания заявки.
     * @return {@link RequestDto} - представление заявки для перемещения между слоями, приложениями.
     */
    @Override
    public RequestDto create(RequestPayload payload) {
        log.debug("Создание заявки по ПВЗ [{}]. Подал: [{}].", payload.pvzId(), payload.appellantId());
        Request mapped = mapper.create(payload);
        Request saved = repo.save(mapped);
        log.info("Заявка [{}] по ПВЗ [{}] успешно создана. Подал: [{}].", saved.getId(), saved.getPvzId(), saved.getAppellantId());
        return mapper.read(saved);
    }

    /**
     * Получение страницы заявок с фильтрацией.
     *
     * @param page номер страницы.
     * @param size размер выборки.
     * @param filter фильтр заявок.
     * @return {@link PageDto} с {@link RequestDto} - представление страницы и заявок для передачи между слоями, приложениями.
     */
    @Override
    public PageDto<RequestDto> readAll(int page, int size, RequestFilter filter) {
        Pageable pageable = PageRequest.of(page, size);
        Specification<Request> spec = configureSpecifications(filter);
        Page<Request> requestPage = repo.findAll(spec, pageable);
        return mapper.readPage(requestPage);
    }

    /**
     * Настройка спецификаций для фильтрации заявок.
     *
     * @param filter фильтр, параметры которого и используются для настройки спецификаций.
     * @return {@link Specification} - спецификация, используемая для фильтрации заявок.
     */
    private Specification<Request> configureSpecifications(RequestFilter filter) {
        Specification<Request> spec = RequestSpecifications.hasPvzId(filter.pvzId());
        spec = spec
                .and(RequestSpecifications.hasAppellantId(filter.appellantId()))
                .and(RequestSpecifications.likeSubject(filter.subject()))
                .and(RequestSpecifications.hasStatus(filter.requestStatus()));
        return spec;
    }

    /**
     * Получение определенной заявки по идентификатору.
     *
     * @param id идентификатор заявки.
     * @return {@link RequestDto} - представление заявки для перемещения между слоями, приложениями.
     */
    @Override
    public RequestDto read(long id) {
        log.debug("Получение заявки [{}].", id);
        return repo.findById(id).map(mapper::read)
                .orElseThrow(() -> new RequestNotFoundException("Заявка [%S] не найдена.".formatted(id)));
    }

    /**
     * Метод для обновления определенной заявки по ID с полезной нагрузкой.
     * @return {@link RequestDto} - представление заявки для перемещения между слоями, приложениями.
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