package com.supvz.requests_service.repo;

import com.supvz.requests_service.entity.Request;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

import java.util.UUID;

/*
Репозиторий для работы с запросами.
 */
public interface RequestRepository extends CrudRepository<Request, Long> {
    @Query(value = """
            FROM Request r WHERE
            (:pvzId IS NULL OR r.pvzId = :pvzId) AND
            (:appellantId IS NULL OR r.appellantId = :appellantId)
            """)
    Page<Request> findAll(
            @Param("pvzId") Integer pvzId,
            @Param("appellantId") UUID appellantId,
            Pageable pageable);
}
