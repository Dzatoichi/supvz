package com.supvz.requests_service.repo;

import com.supvz.requests_service.core.enums.AssignmentAction;
import com.supvz.requests_service.core.enums.RequestStatus;
import com.supvz.requests_service.model.entity.Request;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

/**
 * Репозиторий заявок.
 */
public interface RequestRepository extends CrudRepository<Request, Long>, JpaSpecificationExecutor<Request> {

    @Query(value = """
            SELECT COUNT(*) FROM request_assignments ra WHERE
            ra.request_id = :requestId AND
            ra.action = :action
            """, nativeQuery = true)
    int countOfAssignmentsByRequestIdAndStatus(
            @Param("requestId") Long requestId, AssignmentAction action);
}