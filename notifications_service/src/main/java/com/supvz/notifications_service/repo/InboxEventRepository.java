package com.supvz.notifications_service.repo;

import com.supvz.notifications_service.entity.InboxEvent;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface InboxEventRepository extends CrudRepository<InboxEvent, UUID> {
}
