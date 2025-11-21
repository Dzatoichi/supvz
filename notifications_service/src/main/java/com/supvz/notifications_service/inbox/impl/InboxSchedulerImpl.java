package com.supvz.notifications_service.inbox.impl;

import com.supvz.notifications_service.model.entity.InboxEvent;
import com.supvz.notifications_service.inbox.InboxEventService;
import com.supvz.notifications_service.inbox.InboxScheduler;
import com.supvz.notifications_service.service.EventProcessingService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class InboxSchedulerImpl implements InboxScheduler {
    private final InboxEventService inboxEventService;
    private final EventProcessingService processingService;

    @Value("${app.inbox.polling.to_process_by_time.number}")
    private Integer batchSize;

//    todo: делэй вынести в проперти. @Scheduled(fixedDelayString = "${app.inbox.polling.delay-ms:10000}")
    @Override
    @Scheduled(fixedDelay = 10000)
    public void poll() {
        log.debug("Polling inbox events.");
        List<InboxEvent> events = inboxEventService.readFirstUnprocessed(batchSize);
//        todo: проблема конкурентности. если много реплик, то мб что они в один момент возьмут тот же батч,
//        todo: оба зарезервируют и обработают. дубли. Надо подумать о том, как за один запрос сделать апдейт reserve_to
//        todo: и получить ивенты
        List<UUID> eventsIds = reserveEvents(events);
//        todo: нет проверки на пустой список.
        for (UUID eventId : eventsIds) {
//            todo: сделать try-catch. Если один ивент упадет -- весь полер остановится
            processingService.processNotification(eventId);
        }
    }

    private List<UUID> reserveEvents(List<InboxEvent> events) {
        List<UUID> eventsIds = events.stream().map(InboxEvent::getEventId).toList();
        log.debug("Reserve events {}.", eventsIds.isEmpty() ? "[EMPTY LIST]" : eventsIds);
//        todo: неправильные логи. если список большой, то может нагрузить логи текстом. придумать лучше. Допустим длину списка.
        for (InboxEvent event : events) {
//        todo: если я получаю батч, тогда и резервировать надо батчем. тоже проблема конкуренции и плохо для производительности
            inboxEventService.reserveEvent(event);
        }
        return eventsIds;
    }
}
