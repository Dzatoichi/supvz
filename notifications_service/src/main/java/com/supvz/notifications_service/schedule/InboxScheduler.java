package com.supvz.notifications_service.schedule;

import com.supvz.notifications_service.service.processor.InboxProcessor;
import com.supvz.notifications_service.service.entity.InboxService;
import com.supvz.notifications_service.model.entity.EventIdTypeProjection;
import com.supvz.notifications_service.model.entity.InboxEventType;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.Executor;
import java.util.function.Function;
import java.util.stream.Collectors;

/**
 * Планировщик обработки и очистки событий во входящем ящике (Inbox).
 * <p>
 * Регулярно выполняет две задачи:
 * <ul>
 *   <li><b>Обработка</b>: получает резервированный батч непроцессированных событий из таблицы {@code inbox},
 *       делегирует их обработку соответствующим {@link InboxProcessor} в отдельных потоках.</li>
 *   <li><b>Очистка</b>: удаляет события, помеченные для удаления (поле {@code clean_after} уже в прошлом),
 *       чтобы предотвратить накопление "мертвых" записей.</li>
 * </ul>
 * <p>
 * Использует паттерн <b>Strategy</b> через {@code Map<InboxEventType, InboxProcessor>} для маршрутизации
 * событий разных типов к соответствующим обработчикам.
 * <p>
 * Обработка событий выполняется асинхронно с помощью настроенного {@link Executor},
 * что обеспечивает параллельную обработку и высокую пропускную способность.
 */
@Slf4j
@Component
public class InboxScheduler {
    private final InboxService inboxService;
    private final Executor eventExecutor;
    private final Map<InboxEventType, InboxProcessor> processors;
    @Value("${app.inbox.schedule.processing.batch-size}")
    private Integer processingBatchSize;
    @Value("${app.inbox.schedule.cleaning.batch-size}")
    private Integer cleaningBatchSize;

    /**
     * Конструктор, инициализирующий зависимости.
     */
    public InboxScheduler(
            InboxService inboxService,
            Executor eventExecutor,
            List<InboxProcessor> processorList
    ) {
        this.inboxService = inboxService;
        this.eventExecutor = eventExecutor;
        this.processors = processorList.stream()
                .collect(Collectors.toMap(InboxProcessor::getType, Function.identity()));
    }

    /**
     * Запускает обработку непроцессированных событий из входящего ящика.
     * Каждое событие резервируется и передаётся в пул потоков для асинхронной обработки
     * соответствующим {@link InboxProcessor}.
     */
    @Scheduled(fixedDelayString = "${app.inbox.schedule.processing.delay-ms}")
    public void process() {
        log.debug("По расписанию метод [PROCESS] inbox событий.");
        List<EventIdTypeProjection> reservedBatch = inboxService.readAndReserveUnprocessedBatch(processingBatchSize);
        if (!reservedBatch.isEmpty()) {
            log.debug("Найдены и зарезервированы события. Размер резервированного батча: [{}]", reservedBatch.size());
            for (EventIdTypeProjection event : reservedBatch) {
                eventExecutor.execute(() ->
                        processors.get(event.getEventType()).process(event.getEventId()));
            }
        }
    }

    /**
     * Запускает очистку проваленных событий из входящего ящика.
     * Это предотвращает накопление "зависших" событий, которые не могут быть успешно обработаны.
     */
    @Scheduled(fixedDelayString = "${app.inbox.schedule.cleaning.delay-ms}")
    public void clean() {
        log.debug("По расписанию метод [CLEAN] inbox событий.");
        List<UUID> batch = inboxService.deleteFailedBatch(cleaningBatchSize);
        if (!batch.isEmpty())
            log.debug("Отмеченные для очистки inbox события успешно удалены. Размер удаленного батча: [{}].", batch.size());
    }
}