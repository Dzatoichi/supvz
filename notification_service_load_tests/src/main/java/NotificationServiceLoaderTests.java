import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;
import java.util.concurrent.TimeoutException;

public class NotificationServiceLoaderTests {
    private static Connection connection;
    private static String userName;
    private static String userPass;
    private static String virtualHost;
    private static String hostName;
    private static int portNumber;

    public static void main(String[] args) throws IOException, TimeoutException {
        try {
            parseEnv();
            int rate = Integer.parseInt(System.getProperty("rate"));
            int count = Integer.parseInt(System.getProperty("count"));
            int delayMs = Integer.parseInt(System.getProperty("delayMs"));

            Connection connection = getConnection(userName, userPass, virtualHost, hostName, portNumber);
            for (int i = 0; i < count; i++) {
                connection.

            }
        } catch (NumberFormatException ex) {
            System.err.println("Системные переменные не получить запарсить браток.");
        } catch (IOException | TimeoutException ex) {
            System.err.println("Что-то пошло не так: %s".formatted(ex.getMessage()));
        } finally {
            getConnection(userName, userPass, virtualHost, hostName, portNumber).close();
        }

    }

    private static void parseEnv() {
        userName = System.getProperty("RABBITMQ_DEFAULT_USER");
        userPass = System.getProperty("RABBITMQ_DEFAULT_PASS");
        virtualHost = System.getProperty("RABBITMQ_DEFAULT_VHOST");
        hostName = System.getProperty("RABBITMQ_HOST");
        portNumber = Integer.parseInt(System.getProperty("RABBITMQ_PORT"));
    }

    private static Connection getConnection(String userName, String userPass, String virtualHost, String hostName, int portNumber) throws IOException, TimeoutException {
        if (connection == null) {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setUsername(userName);
            factory.setPassword(userPass);
            factory.setVirtualHost(virtualHost);
            factory.setHost(hostName);
            factory.setPort(portNumber);
            connection = factory.newConnection();
        }
        return connection;
    }
}
