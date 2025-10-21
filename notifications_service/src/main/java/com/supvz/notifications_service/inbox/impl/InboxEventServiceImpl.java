package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.core.MessageDto;
import com.supvz.notifications_service.entity.InboxEvent;
import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.mapper.InboxEventMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class InboxEventServiceImpl implements InboxEventService {
    private final InboxEventMapper mapper;

    @Override
    public InboxEvent create(MessageDto messageDto) {
        log.info("CREATE INBOX EVENT [{}].", messageDto.payload());
        log.info("INBOX EVENT [{}] IS CREATED.", UUID.randomUUID());
        return null;
    }
}
