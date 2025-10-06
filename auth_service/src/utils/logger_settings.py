import os
import sys

from loguru import logger

from src.settings.config import settings

LOG_LEVEL = settings.LOG_LEVEL
LOG_TO_CONSOLE = settings.LOG_TO_CONSOLE
LOGS_DIR = settings.LOGS_DIR


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
    rotation="100 KB",
    retention="10 days",
    level=LOG_LEVEL,
    enqueue=True,
)
