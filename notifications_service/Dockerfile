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
COPY --from=builder /app/target/notifications_service-0.0.1-SNAPSHOT.jar app.jar

RUN apk add --no-cache curl

ENTRYPOINT ["java", "-Dspring.profiles.active=prod", "-jar", "app.jar"]

# todo: создать юзера с правами. короче по бест практис сделать