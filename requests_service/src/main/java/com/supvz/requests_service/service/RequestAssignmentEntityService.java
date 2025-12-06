package com.supvz.requests_service.service;

import com.supvz.requests_service.core.exception.RequestAssignmentNotFoundException;
import com.supvz.requests_service.model.dto.PageDto;
import com.supvz.requests_service.model.dto.RequestAssignmentDto;
import com.supvz.requests_service.model.dto.RequestAssignmentPayload;
import com.supvz.requests_service.model.dto.RequestAssignmentUpdatePayload;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import com.supvz.requests_service.mapper.RequestAssignmentMapper;
import com.supvz.requests_service.repo.RequestAssignmentRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Реализация сервиса для обработки ответов на заявки.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class RequestAssignmentEntityService implements RequestAssignmentService {
    private final RequestAssignmentMapper mapper;
    private final RequestAssignmentRepository repo;
    private final RequestService requestService;


    /**
     * Метод для создания ответа-сущности по полученной нагрузке.
     */
    @Override
    @Transactional
    public RequestAssignmentDto create(long requestId, RequestAssignmentPayload payload) {
        log.info("Создание ответа на заявку [{}]. Мастер: [{}].", requestId, payload.handymanId());
        Request request = requestService.get(requestId);
        RequestAssignment mapped = mapper.create(request, payload);
        RequestAssignment saved = repo.save(mapped);
        log.info("Ответ [{}] на заявку успешно создан мастером [{}].", saved.getRequest().getId(), saved.getHandymanId());
        return mapper.read(saved);
    }
//    todo: конфликт



    /**
     * Метод для чтения страницы ответов на заявку с пагинацией.
     */
    @Override
    public PageDto<RequestAssignmentDto> readAll(long requestId, int pageNumber, int size) {
        Pageable pageable = PageRequest.of(pageNumber, size);
        Page<RequestAssignment> page = repo.findAll(requestId, pageable);
        return mapper.readPage(page);
    }
//    todo: фильтрация

    /**
     * Метод для чтения определенного ответа на заявку по ID.
     */
    @Override
    public RequestAssignmentDto read(long id) {
        log.debug("Получение ответа [{}] на заявку.", id);
        return repo.findById(id)
                .map(mapper::read)
                .orElseThrow(() -> new RequestAssignmentNotFoundException
                        ("Ответ [%s] на заявку не найден.".formatted(id)));
    }


    /**
     * Метод для обновления определенного ответа на заявку по ID с полезной нагрузкой.
     */
    @Override
    public RequestAssignmentDto update(long id, RequestAssignmentUpdatePayload payload) {
        log.debug("Обновление ответа [{}] на заявку.", id);
        RequestAssignment found = repo.findById(id)
                .orElseThrow(() -> new RequestAssignmentNotFoundException
                        ("Ответ [%s] на заявку не найден.".formatted(id)));
        RequestAssignment mapped = mapper.update(found, payload);
        RequestAssignment saved = repo.save(mapped);
        log.info("Ответ [{}] на заявку успешно обновлен.", saved.getId());
        return mapper.read(saved);
    }


    /**
     * Метод для удаления определенного ответа на заявку по ID.
     */
    @Override
    @Transactional
    public void delete(long id) {
        log.debug("Удаление ответа [{}] на заявку.", id);
        RequestAssignment found = repo.findById(id)
                .orElseThrow(() -> new RequestAssignmentNotFoundException
                        ("Ответ [%s] на заявку не найден.".formatted(id)));
        repo.delete(found);
        log.info("Ответ [{}] на заявку успешно удалён.", id);
    }
//    todo: какой смысл вообще делать две строки, если можно удалить за одно обращение к бд?
//     без поиска и прочей чепухи? взял и удалил. если не удалил, значит, не нашел, тогда выкинул ошибку
}
// TODO: логи исправить и перевести
