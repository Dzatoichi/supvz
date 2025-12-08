package com.supvz.requests_service.mapper.action;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.model.entity.RequestAssignment;
import com.supvz.requests_service.service.RequestService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

/**
 * Реализация {@link ActionMapper}. Является паттерном Strategy.
 * <br/>
 * Занимается обработкой ответа, заявки в случае определенного действия {@link AssignmentAction}
 *
 * <p>Данный маппер является реализацией поведения {@code  AssignmentAction.reject}</p>
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class RejectActionMapper implements ActionMapper {
    private final RequestService requestService;
    /**
     * Маппинг-обработка для поведения действия "Отказ ({@code AssignmentAction.reject})".
     * <br/>
     * Заявка отмечается как отмененная.
     *
     * @param assignment сущность ответа на заявку.
     * @return {@link RequestAssignment} - обработанная сущность ответа на заявку с обработанной заявкой.
     */
    @Override
    public RequestAssignment map(RequestAssignment assignment) {
        requestService.setStatus(assignment.getRequest(), RequestStatus.pending);
        assignment.setProcessedAt(LocalDateTime.now());
        assignment.setAction(this.getType());
        return assignment;
    }

    /**
     * Метод для реализации паттерна Strategy
     * @return {@link AssignmentAction} - тип, с которым работает данный маппер.
     */
    @Override
    public AssignmentAction getType() {
        return AssignmentAction.reject;
    }
}