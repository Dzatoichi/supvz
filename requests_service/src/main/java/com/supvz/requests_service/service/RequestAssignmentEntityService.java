package com.supvz.requests_service.service;

import com.supvz.requests_service.core.exception.RequestAssignmentInvalidPayloadException;
import com.supvz.requests_service.model.entity.enums.AssignmentAction;
import com.supvz.requests_service.model.entity.enums.RequestStatus;
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
 * Реализация сервиса для обработки обращений на заявки.
 * Отвечает за бизнес-логику обращений на заявки. Слой, что работает с сущностями напрямую.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class RequestAssignmentEntityService implements RequestAssignmentService {
    private final RequestAssignmentMapper mapper;
    private final RequestAssignmentRepository repo;
    private final RequestService requestService;

    /**
     * Создание сущности обращения на заявку.
     *
     * @param payload полезная нагрузка для создания обращения на заявку.
     * @return {@link RequestAssignmentDto} - представление обращения на заявку для перемещения между слоями, приложениями.
     */
    @Override
    @Transactional
    public RequestAssignmentDto create(RequestAssignmentPayload payload) {
        log.info("Создание обращения на заявку [{}]. Мастер: [{}].", payload.requestId(), payload.handymanId());
        if (repo.existsByRequestIdAndHandymanId(payload.requestId(), payload.handymanId()))
            throw new RequestAssignmentConflictException("Мастер [%s] уже взял или брал в работу заявку [%s].".formatted(payload.handymanId(), payload.requestId()));
        Request request = requestService.assign(payload.requestId());
        RequestAssignment mapped = mapper.create(request, payload);
        RequestAssignment saved = repo.save(mapped);
        log.info("Обращение [{}] на заявку [{}] успешно создано мастером [{}].", saved.getId(), payload.requestId(), payload.handymanId());
        return mapper.read(saved);
    }

    /**
     * Получение страницы обращений на заявки с фильтрацией.
     *
     * @param page   номер страницы.
     * @param size   размер выборки.
     * @param filter фильтр обращений на заявки.
     * @return {@link PageDto} с {@link RequestAssignmentDto} - представление страницы обращений на заявки для передачи между слоями, приложениями.
     */
    @Override
    public PageDto<RequestAssignmentDto> readAll(int page, int size, RequestAssignmentFilter filter) {
        Pageable pageable = PageRequest.of(page, size);
        Specification<RequestAssignment> spec = configureSpecifications(filter);
        Page<RequestAssignment> assignmentPage = repo.findAll(spec, pageable);
        return mapper.readPage(assignmentPage);
    }


    /**
     * Настройка спецификаций для фильтрации обращений на заявки.
     *
     * @param filter фильтр, параметры которого и используются для настройки спецификаций.
     * @return {@link Specification} - спецификация, используемая для фильтрации обращений.
     */
    private Specification<RequestAssignment> configureSpecifications(RequestAssignmentFilter filter) {
        Specification<RequestAssignment> spec = RequestAssignmentSpecifications.hasRequestId(filter.requestId());
        spec = spec
                .and(RequestAssignmentSpecifications.hasHandymanId(filter.handymanId()))
                .and(RequestAssignmentSpecifications.hasAction(filter.action()));
        return spec;
    }

    /**
     * Получение определенного обращения на заявку по его идентификатору.
     *
     * @param id идентификатор обращения на заявку.
     * @return {@link RequestAssignmentDto} - представление обращения на заявку для перемещения между слоями, приложениями.
     */
    @Override
    public RequestAssignmentDto read(long id) {
        log.debug("Получение обращения [{}] на заявку.", id);
        return repo.findById(id)
                .map(mapper::read)
                .orElseThrow(() -> new RequestAssignmentNotFoundException
                        ("Обращение [%s] на заявку не найдено.".formatted(id)));
    }

    /**
     * Обновление определенного обращения на заявку по его идентификатору.
     *
     * @param id      идентификатор обращения на заявку.
     * @param payload полезная нагрузка для обновления обращения на заявку.
     * @return {@link RequestAssignmentDto} - представление обращения на заявку для перемещения между слоями, приложениями.
     */
    @Override
    @Transactional
    public RequestAssignmentDto update(long id, RequestAssignmentUpdatePayload payload) {
        log.debug("Обновление обращения [{}] на заявку.", id);
        RequestAssignment assignment = repo.findById(id)
                .orElseThrow(() -> new RequestAssignmentNotFoundException("Обращение [%s] на заявку не найдено.".formatted(id)));
        if (payload.action() != null) {
            processAction(assignment, payload.action());
        }
        RequestAssignment mapped = mapper.update(assignment, payload);
        RequestAssignment saved = repo.save(mapped);
        log.info("Обращение [{}] на заявку успешно обновлено.", saved.getId());
        return mapper.read(saved);
    }

    /**
     * Вспомогательный метод для обработки действия обращения.
     * <br/>
     * Метод обрабатывает в зависимости от {@code AssignmentAction}.
     * <br/>
     * Например, если обращение на заявку с действием отмены выполнения и, например, данной заявкой занимается еще как минимум
     * один человек, то заявка остается с тем статусом, что у нее уже есть.
     *
     * @param assignment сущность обращения на заявку.
     * @param action     действие, которое отвечает, какой статус приобретет заявка.
     */
    private void processAction(RequestAssignment assignment, AssignmentAction action) {
        Long assignmentId = assignment.getId();
        if (action == AssignmentAction.system_cancel) {
            throw new RequestAssignmentInvalidPayloadException("Обращение [%s] с типом '%s' не может быть выполнено по запросу мастера."
                    .formatted(assignmentId, AssignmentAction.system_cancel.name()));
        }
        Request request = assignment.getRequest();
        long handymanId = assignment.getHandymanId();
        Long requestId = request.getId();
        boolean isCancel = action == AssignmentAction.self_cancel;
        RequestStatus targetRequestStatus = action.getTargetRequestStatus();
        if (isCancel && repo.existsByRequestIdAndActionAndIdNot(requestId, AssignmentAction.assign, assignmentId)) {
            log.warn("Мастер [{}] отменяет обращение [{}], но заявка [{}] остается в работе у других.", handymanId, assignmentId, requestId);
            targetRequestStatus = request.getStatus();
        }
        if (action == AssignmentAction.complete || action == AssignmentAction.reject) {
            int updated = repo.setActiveAssignmentsAsSystemCancelByRequestIdInsteadAssignmentId(requestId, assignmentId);
            if (updated > 0)
                log.debug("Так как заявка [{}] отмечается как выполненная, остальные обращения отмечаются как системно отмененные.", requestId);
        }
        requestService.setStatus(request, targetRequestStatus);
    }
}