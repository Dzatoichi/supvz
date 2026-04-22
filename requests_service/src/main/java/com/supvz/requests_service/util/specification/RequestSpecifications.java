package com.supvz.requests_service.util.specification;

import com.supvz.requests_service.model.entity.enums.RequestStatus;
import com.supvz.requests_service.model.entity.Request;
import org.springframework.data.jpa.domain.Specification;

/**
 * Спецификации для фильтрации сущностей {@link Request}.
 */
public class RequestSpecifications {
    /**
     * Создаёт спецификацию для фильтрации по идентификатору ПВЗ.
     *
     * @param pvzId идентификатор ПВЗ; если {@code null}, применяется пустое условие
     * @return спецификация, соответствующая заданному {@code pvzId}
     */
    public static Specification<Request> hasPvzId(Integer pvzId) {
        return (root, _, cb) -> {
            if (pvzId == null) return cb.conjunction();
            return cb.equal(root.get("pvzId"), pvzId);
        };
    }

    /**
     * Создаёт спецификацию для фильтрации по идентификатору заявителя.
     *
     * @param appellantId идентификатор заявителя; если {@code null}, возвращает {@code null}
     * @return спецификация или {@code null}, если параметр не задан
     */
    public static Specification<Request> hasAppellantId(Long appellantId) {
        return (root, _, cb) -> {
            if (appellantId == null) return null;
            return cb.equal(root.get("appellantId"), appellantId);
        };
    }

    /**
     * Создаёт спецификацию для частичного совпадения по теме запроса.
     *
     * @param subject тема запроса; если {@code null}, возвращает {@code null}
     * @return спецификация или {@code null}, если параметр не задан
     */
    public static Specification<Request> likeSubject(String subject) {
        return (root, _, cb) -> {
            if (subject == null) return null;
            return cb.like(root.get("subject"), subject);
        };
    }

    /**
     * Создаёт спецификацию для фильтрации по статусу запроса.
     *
     * @param status статус запроса; если {@code null}, возвращает {@code null}
     * @return спецификация или {@code null}, если параметр не задан
     */
    public static Specification<Request> hasStatus(RequestStatus status) {
        return (root, _, cb) -> {
            if (status == null) return null;
            return cb.equal(root.get("status"), status);
        };
    }
}