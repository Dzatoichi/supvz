package com.supvz.notifications_service_load_tests;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.MessageProperties;
import com.supvz.notifications_service_load_tests.core.InboxEventPayload;
import com.supvz.notifications_service_load_tests.core.InboxEventType;
import com.supvz.notifications_service_load_tests.core.NotificationPayload;
import com.supvz.notifications_service_load_tests.core.NotificationType;

import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;

public class NotificationsLoadGenerator {

    private static Connection connection;

    private static String username;
    private static String password;
    private static String virtualHost;
    private static String host;
    private static int port;
    private static String exchange;
    private static String routingKey;

    private static final ObjectMapper json = new ObjectMapper();

    public static void main(String[] args) {
        parseEnv();
        int totalMessages = Integer.parseInt(System.getProperty("count", "100"));
        int threads = Integer.parseInt(System.getProperty("threads", "1"));
        int rate = Integer.parseInt(System.getProperty("rate", "10"));
        int delayPerMessageMs = Math.max(1, 1000 / (rate / threads));
        System.out.printf("""
                Starting load generator:
                totalMessages = %d
                threads = %d
                rate = %d msg/s
                delayPerMessageMs = %d
                %n""", totalMessages, threads, rate, delayPerMessageMs);
        try {
            connection = createConnection();
            ExecutorService executor = Executors.newFixedThreadPool(threads);
            List<Long> latencies = Collections.synchronizedList(new ArrayList<>());
            Instant start = Instant.now();
            int perThread = totalMessages / threads;
            List<Future<?>> futures = new ArrayList<>();
            for (int t = 0; t < threads; t++) {
                futures.add(executor.submit(() -> {
                    try (Channel channel = connection.createChannel()) {
                        for (int i = 0; i < perThread; i++) {
                            InboxEventPayload event = randomEvent();
                            byte[] body = json.writeValueAsBytes(event);
                            long sendStart = System.nanoTime();
                            channel.basicPublish(
                                    exchange,
                                    routingKey,
                                    MessageProperties.PERSISTENT_TEXT_PLAIN,
                                    body
                            );
                            long elapsed = System.nanoTime() - sendStart;
                            latencies.add(elapsed);
                            Thread.sleep(delayPerMessageMs);
                        }
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }));
            }
            for (Future<?> f : futures) {
                f.get();
            }
            Instant end = Instant.now();
            executor.shutdown();
            printStats(latencies, Duration.between(start, end), totalMessages);
        } catch (Exception e) {
            System.err.println("CONNECTION CREATE");
            e.printStackTrace();
        } finally {
            closeConnection();
        }
    }

    private static void parseEnv() {
        username = System.getenv("RABBITMQ_DEFAULT_USER");
        password = System.getenv("RABBITMQ_DEFAULT_PASS");
        virtualHost = System.getenv("RABBITMQ_DEFAULT_VHOST");
        host = System.getenv("RABBITMQ_HOST");
        port = Integer.parseInt(System.getenv("RABBITMQ_PORT"));
        exchange = System.getenv("MESSAGING_INBOX_EXCHANGE");
        routingKey = System.getenv("MESSAGING_INBOX_ROUTING_KEY");
    }

    private static Connection createConnection() throws IOException, TimeoutException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setUsername(username);
        factory.setPassword(password);
        factory.setVirtualHost(virtualHost);
        factory.setHost(host);
        factory.setPort(port);
        return factory.newConnection();
    }

    private static void closeConnection() {
        try {
            if (connection != null && connection.isOpen())
                connection.close();
        } catch (Exception ignored) {
            System.err.println("CONNECTION CLOSE");
        }
    }

    // ------------ METRICS ------------
    private static void printStats(List<Long> latencies, Duration elapsed, int total) {

        latencies.sort(Long::compare);
        long p50 = percentile(latencies, 50);
        long p95 = percentile(latencies, 95);
        long p99 = percentile(latencies, 99);

        double seconds = elapsed.toMillis() / 1000.0;
        double throughput = total / seconds;

        System.out.printf("""
                === Load Test Result ===
                Total messages: %d
                Total time: %.2f sec
                Throughput: %.2f msg/sec

                Latencies:
                AVG = %.2f ms
                P50 = %.2f ms
                P95 = %.2f ms
                P99 = %.2f ms
                """,
                total,
                seconds,
                throughput,
                avg(latencies) / 1_000_000.0,
                p50 / 1_000_000.0,
                p95 / 1_000_000.0,
                p99 / 1_000_000.0
        );
    }

    private static long percentile(List<Long> list, int p) {
        int index = (int) Math.ceil(p / 100.0 * list.size()) - 1;
        return list.get(Math.max(0, index));
    }

    private static double avg(List<Long> list) {
        return list.stream().mapToLong(i -> i).average().orElse(0);
    }

    // ------------ RANDOM EVENT GENERATOR ------------

    private static InboxEventPayload randomEvent() {

        NotificationPayload payload = new NotificationPayload(
                randomEnum(NotificationType.class),
                "user-" + ThreadLocalRandom.current().nextInt(1, 10000),
                randomBody(),
                randomSubject()
        );

        String payloadJson;
        try {
            payloadJson = json.writeValueAsString(payload);
        } catch (Exception e) {
            payloadJson = "{}";
        }

        return new InboxEventPayload(
                UUID.randomUUID(),
                randomEnum(InboxEventType.class),
                payloadJson
        );
    }

    private static String randomBody() {
        String[] variants = {
                "Hello from load test",
                "Notification example",
                "Stress test message",
                "Performance load event"
        };
        return variants[ThreadLocalRandom.current().nextInt(variants.length)];
    }

    private static String randomSubject() {
        String[] variants = {
                "Load Subject",
                "Important Notification",
                "Test Subject",
                "Alert Test"
        };
        return variants[ThreadLocalRandom.current().nextInt(variants.length)];
    }

    private static <T extends Enum<?>> T randomEnum(Class<T> cls) {
        T[] constants = cls.getEnumConstants();
        return constants[ThreadLocalRandom.current().nextInt(constants.length)];
    }
}
