from loguru import logger
import sys
import os

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

logger.remove()

# Вывод в консоль
logger.add(
    sys.stdout,
    colorize=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[client_ip]}:{extra[client_port]} - "
    '"{extra[method]} {extra[path]} HTTP/{extra[http_version]}" {extra[status_code]}',
    level="INFO",
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
