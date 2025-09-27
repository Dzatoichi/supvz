from loguru import logger
import sys
import os

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

logger.remove()

# В консоль (цветной, для разработки)
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time}</green> <level>{message}</level>",
    level="INFO",
)

# В файл (JSON, для ELK)
logger.add(
    f"{LOGS_DIR}/app.log",
    serialize=True,
    rotation="10 MB",
    retention="10 days",
    level="INFO",
)
