import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", "True").lower() in ("true", "1", "yes")
LOGS_DIR = os.getenv("LOGS_DIR", "logs")

os.makedirs(LOGS_DIR, exist_ok=True)

logger.remove()

if LOG_TO_CONSOLE:
    # Для разработки — формат в консоль
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | {message} | {extra}",
        level=LOG_LEVEL,
    )

# Для продакшена — JSON-логи в файл (подходит для ELK)
logger.add(
    f"{LOGS_DIR}/app.log",
    serialize=True,
    rotation="10 MB",
    retention="10 days",
    level=LOG_LEVEL,
    enqueue=True,
)
