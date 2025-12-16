FROM eclipse-temurin:24-jdk-alpine as builder

WORKDIR /app
COPY .mvn .mvn
COPY mvnw mvnw
COPY pom.xml .
COPY src src

# Копируем java-агента для инструментации финального образа проекта под стандарт OpenTelemetry
COPY infrastructure/otel_java_agent/opentelemetry-javaagent.jar otel-agent.jar

RUN chmod +x mvnw
RUN ./mvnw clean package -DskipTests

# _________________________________________________________________________

FROM eclipse-temurin:24-jre-alpine

WORKDIR /app
COPY --from=builder /app/target/notifications_service-0.0.1-SNAPSHOT.jar app.jar
COPY --from=builder /app/otel-agent.jar otel-agent.jar

RUN apk add --no-cache curl
RUN mkdir logs

RUN adduser -D -s /sbin/nologin -u 1001 app
RUN chown -R app:app /app/app.jar /app/logs /app/otel-agent.jar
USER app

ENTRYPOINT ["java", "-javaagent:otel-agent.jar", "-jar", "app.jar"]