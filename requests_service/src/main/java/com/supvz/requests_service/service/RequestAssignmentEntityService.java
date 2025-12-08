package com.supvz.requests_service.service;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.core.exception.RequestAssignmentConflictException;
import com.supvz.requests_service.core.exception.RequestAssignmentNotFoundException;
import com.supvz.requests_service.core.filter.RequestAssignmentFilter;
import com.supvz.requests_service.model.dto.*;
import com.supvz.requests_service.model.entity.Request;
import com.supvz.requests_service.model.entity.RequestAssignment;
import com.supvz.requests_service.mapper.RequestAssignmentMapper;
import com.supvz.requests_service.repo.RequestAssignmentRepository;
import com.supvz.requests_service.util.specification.RequestAssignmentSpecifications;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Реализация сервиса для обработки ответов на заявки.
 * Отвечает за бизнес-логику ответов на заявки. Слой, что работает с сущностями напрямую.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class RequestAssignmentEntityService implements RequestAssignmentService {
    private final RequestAssignmentMapper mapper;
    private final RequestAssignmentRepository repo;
    private final RequestService requestService;

    /**
     * Создание сущности ответа на заявку.
     *
     * @param payload полезная нагрузка для создания ответа на заявку.
     * @return {@link RequestAssignmentDto} - представление ответа на заявку для перемещения между слоями, приложениями.
     */
    @Override
    @Transactional
    public RequestAssignmentDto create(RequestAssignmentPayload payload) {
        log.info("Создание ответа на заявку [{}]. Мастер: [{}].", payload.requestId(), payload.handymanId());
        if (repo.existsByRequestIdAndHandymanId(payload.requestId(), payload.handymanId()))
            throw new RequestAssignmentConflictException("Мастер [%s] уже взял или брал в работу заявку [%s].".formatted(payload.handymanId(), payload.requestId()));
        Request request = requestService.assign(payload.requestId());
        RequestAssignment mapped = mapper.create(request, payload);
        RequestAssignment saved = repo.save(mapped);
        log.info("Ответ [{}] на заявку [{}] успешно создан мастером [{}].", saved.getId(), payload.requestId(), payload.handymanId());
        return mapper.read(saved);
    }

    /**
     * Получение страницы ответов на заявки с фильтрацией.
     *
     * @param page   номер страницы.
     * @param size   размер выборки.
     * @param filter фильтр ответов на заявки.
     * @return {@link PageDto} с {@link RequestAssignmentDto} - представление страницы и ответов на заявки для передачи между слоями, приложениями.
     */
    @Override
    public PageDto<RequestAssignmentDto> readAll(int page, int size, RequestAssignmentFilter filter) {
        Pageable pageable = PageRequest.of(page, size);
        Specification<RequestAssignment> spec = configureSpecifications(filter);
        Page<RequestAssignment> assignmentPage = repo.findAll(spec, pageable);
        return mapper.readPage(assignmentPage);
    }


    /**
     * Настройка спецификаций для фильтрации ответов на заявки.
     *
     * @param filter фильтр, параметры которого и используются для настройки спецификаций.
     * @return {@link Specification} - спецификация, используемая для фильтрации заявок.
     */
    private Specification<RequestAssignment> configureSpecifications(RequestAssignmentFilter filter) {
        Specification<RequestAssignment> spec = RequestAssignmentSpecifications.hasRequestId(filter.requestId());
        spec = spec
                .and(RequestAssignmentSpecifications.hasHandymanId(filter.handymanId()))
                .and(RequestAssignmentSpecifications.hasAction(filter.action()));
        return spec;
    }

    /**
     * Получение определенного ответа на заявку по его идентификатору.
     *
     * @param id идентификатор ответа на заявку.
     * @return {@link RequestAssignmentDto} - представление ответа на заявку для перемещения между слоями, приложениями.
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
     * Обновление определенного ответа на заявку по его идентификатору.
     *
     * @param id      идентификатор ответа на заявку.
     * @param payload полезная нагрузка для обновления ответа на заявку.
     * @return {@link RequestAssignmentDto} - представление ответа на заявку для перемещения между слоями, приложениями.
     */
    @Override
    @Transactional
    public RequestAssignmentDto update(long id, RequestAssignmentUpdatePayload payload) {
        log.debug("Обновление ответа [{}] на заявку.", id);
        RequestAssignment assignment = repo.findById(id)
                .orElseThrow(() -> new RequestAssignmentNotFoundException("Ответ [%s] на заявку не найден.".formatted(id)));
        if (payload.action() != null) {
            processAction(assignment, payload.action());
        }
        RequestAssignment mapped = mapper.update(assignment, payload);
        RequestAssignment saved = repo.save(mapped);
        log.info("Ответ [{}] на заявку успешно обновлен.", saved.getId());
        return mapper.read(saved);
    }

    private void processAction(RequestAssignment assignment, AssignmentAction action) {
        Long assignmentId = assignment.getId();
        Request request = assignment.getRequest();
        long handymanId = assignment.getHandymanId();
        Long requestId = request.getId();
        boolean isCancel = action == AssignmentAction.cancel;
        RequestStatus targetRequestStatus = action.getTargetRequestStatus();

        if (isCancel && repo.existsByRequestIdAndActionAndIdNot(requestId, AssignmentAction.assign, assignmentId)) {
            log.warn("Мастер [{}] отменяет ответ [{}], но заявка [{}] остается в работе у других.", handymanId, assignmentId, requestId);
            targetRequestStatus = request.getStatus();
        }
        requestService.setStatus(request, targetRequestStatus);
    }
}