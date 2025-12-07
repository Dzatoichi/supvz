package com.supvz.requests_service.util.specification;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.model.entity.RequestAssignment;
import org.springframework.data.jpa.domain.Specification;

public class RequestAssignmentSpecifications {
    public static Specification<RequestAssignment> hasRequestId(Long requestId) {
        return (root, _, cb) -> {
            if (requestId == null) return cb.conjunction();
            return cb.equal(root.get("request").get("id"), requestId);
        };
    }

    public static Specification<RequestAssignment> hasHandymanId(Long handymanId) {
        return (root, _, cb) -> {
            if (handymanId == null) return null;
            return cb.equal(root.get("handymanId"), handymanId);
        };
    }

    public static Specification<RequestAssignment> hasAction(AssignmentAction action) {
        return (root, _, cb) -> {
            if (action == null) return cb.conjunction();
            return cb.equal(root.get("action"), action);
        };
    }
}
