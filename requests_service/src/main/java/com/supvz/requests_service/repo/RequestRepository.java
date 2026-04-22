package com.supvz.requests_service.repo;

import com.supvz.requests_service.model.entity.Request;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.repository.CrudRepository;

/**
 * Репозиторий заявок.
 */
public interface RequestRepository extends CrudRepository<Request, Long>, JpaSpecificationExecutor<Request> {
}