FROM eclipse-temurin:24-jdk-alpine as builder

WORKDIR /app
COPY .mvn .mvn
COPY mvnw mvnw
COPY pom.xml .
COPY src src

RUN chmod +x mvnw
RUN ./mvnw clean package -DskipTests

# _________________________________________________________________________

FROM eclipse-temurin:24-jre-alpine

WORKDIR /app
COPY --from=builder /app/target/requests_service-0.0.1-SNAPSHOT.jar app.jar

ENTRYPOINT ["java", "-Dspring.profiles.active=prod", "-jar", "app.jar"]