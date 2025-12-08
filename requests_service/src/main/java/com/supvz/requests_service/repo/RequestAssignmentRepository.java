package com.supvz.requests_service.repo;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.model.entity.RequestAssignment;
import jakarta.validation.constraints.NotNull;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

/**
 * Репозиторий ответов на заявки.
 */
public interface RequestAssignmentRepository extends CrudRepository<RequestAssignment, Long>, JpaSpecificationExecutor<RequestAssignment> {
    @Query(value = """
            SELECT EXISTS (
                SELECT 1 FROM request_assignments ra WHERE
                ra.request_id = :requestId AND
                ra.handyman_id = :handymanId
            )
            """, nativeQuery = true)
    boolean existsByRequestIdAndHandymanId(
            @Param("requestId") long requestId,
            @Param("handymanId") long handymanId);

    boolean existsByRequestIdAndActionAndIdNot(Long requestId, AssignmentAction action, Long excludedId);
}
