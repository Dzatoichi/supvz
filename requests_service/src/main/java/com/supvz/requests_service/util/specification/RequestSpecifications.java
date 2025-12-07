package com.supvz.requests_service.util.specification;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.model.entity.Request;
import org.springframework.data.jpa.domain.Specification;

public class RequestSpecifications {
    public static Specification<Request> hasPvzId(Integer pvzId) {
        return (root, _, cb) -> {
            if (pvzId == null) return cb.conjunction();
            return cb.equal(root.get("pvzId"), pvzId);
        };
    }

    public static Specification<Request> hasAppellantId(Long appellantId) {
        return (root, _, cb) -> {
            if (appellantId == null) return null;
            return cb.equal(root.get("appellantId"), appellantId);
        };
    }

    public static Specification<Request> likeSubject(String subject) {
        return (root, _, cb) -> {
            if (subject == null) return null;
            return cb.like(root.get("subject"), subject);
        };
    }

    public static Specification<Request> hasStatus(RequestStatus status) {
        return (root, _, cb) -> {
            if (status == null) return null;
            return cb.equal(root.get("status"), status);
        };
    }
}
