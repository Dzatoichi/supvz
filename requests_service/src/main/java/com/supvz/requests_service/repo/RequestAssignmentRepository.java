package com.supvz.requests_service.repo;

import com.supvz.requests_service.model.entity.enums.AssignmentAction;
import com.supvz.requests_service.model.entity.RequestAssignment;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

/**
 * Репозиторий обращений на заявки.
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
            @Param("handymanId") long handymanId
    );

    boolean existsByRequestIdAndActionAndIdNot(Long requestId, AssignmentAction action, Long excludedId);

    @Modifying
    @Query(value = """
            UPDATE request_assignments ra
            SET action = 'system_cancel'
            WHERE ra.request_id = :requestId
              AND ra.action = 'assign'
              AND ra.id != :assignmentId
            """, nativeQuery = true)
    int setActiveAssignmentsAsSystemCancelByRequestIdInsteadAssignmentId(
            @Param("requestId") Long requestId,
            @Param("assignmentId") Long assignmentId
    );
}
