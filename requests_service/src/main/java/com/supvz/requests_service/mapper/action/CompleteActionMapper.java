package com.supvz.requests_service.mapper.action;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.model.entity.RequestAssignment;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

/**
 * Реализация {@link ActionMapper}. Является паттерном Strategy.
 * <br/>
 * Занимается обработкой ответа, заявки в случае определенного действия {@link AssignmentAction}
 *
 * <p>Данный маппер является реализацией поведения {@code  AssignmentAction.complete}</p>
 */
@Slf4j
@Component
public class CompleteActionMapper implements ActionMapper {
    /**
     * Маппинг-обработка для поведения действия "Выполнено ({@code AssignmentAction.complete})".
     * <br/>
     * Заявка отмечается как выполненная.
     *
     * @param assignment сущность ответа на заявку.
     * @return {@link RequestAssignment} - обработанная сущность ответа на заявку с обработанной заявкой.
     */
    @Override
    public RequestAssignment map(RequestAssignment assignment) {
        assignment.setProcessedAt(LocalDateTime.now());
        assignment.setAction(this.getType());
        assignment.getRequest().setStatus(RequestStatus.completed);
        log.info("Заявка [{}] выполнена. По ответу [{}].",
                assignment.getRequest().getId(), assignment.getId());
        return assignment;
    }

    /**
     * Метод для реализации паттерна Strategy
     *
     * @return {@link AssignmentAction} - тип, с которым работает данный маппер.
     */
    @Override
    public AssignmentAction getType() {
        return AssignmentAction.complete;
    }
}