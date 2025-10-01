from loguru import logger
import sys
import os

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

logger.remove()


# Access-логи (middleware) — с IP
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | {extra[client_ip]}:{extra[client_port]} - "
    '"{extra[method]} {extra[path]} HTTP/{extra[http_version]}" {extra[status_code]}',
    level="INFO",
    filter=lambda record: record["extra"].get("log_type") == "access",
)

# Бизнес-логи — без IP
logger.add(
    sys.stdout,
    format="<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | {level} | {message} | {extra}",
    level="INFO",
    filter=lambda record: record["extra"].get("log_type") == "business",
)

# Вывод файл (JSON)
logger.add(
    f"{LOGS_DIR}/app.log",
    enqueue=True,
    serialize=True,
    rotation="10 MB",
    retention="30 days",
    level="INFO",
)
