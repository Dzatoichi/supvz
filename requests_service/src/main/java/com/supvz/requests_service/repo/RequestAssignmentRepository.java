package com.supvz.requests_service.repo;

import com.supvz.requests_service.model.entity.RequestAssignment;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

/**
 * Репозиторий ответов на заявки.
 */
public interface RequestAssignmentRepository extends CrudRepository<RequestAssignment, Long>, JpaSpecificationExecutor<RequestAssignment> {
}
