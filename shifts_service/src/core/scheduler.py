from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.dao.shift_requestsDAO import ShiftRequestsDAO
from src.database.base import db_helper
from src.services.shift_requests_service import ShiftRequestsService
from src.utils.logger_settings import logger


async def cancel_expired_pending_requests() -> None:
    """
    Отменяет pending запросы, у которых смена уже началась.

    Устанавливает статус cancelled_by_system с соответствующей причиной.
    """
    logger.info("Starting task: cancel_expired_pending_requests")

    try:
        async with db_helper.async_session_maker() as session:
            dao = ShiftRequestsDAO(session=session)
            service = ShiftRequestsService(dao=dao)

            cancelled_count = await service.cancel_expired_requests()

            logger.info(
                "Task completed: cancel_expired_pending_requests",
                cancelled_count=cancelled_count,
                timestamp=datetime.now().isoformat(),
            )
    except Exception as e:
        logger.error(
            "Task failed: cancel_expired_pending_requests",
            error=str(e),
            timestamp=datetime.now().isoformat(),
        )
        raise


async def cleanup_old_requests(months: int = 2) -> None:
    """
    Удаляет старые запросы (кроме approved) старше указанного срока.

    Args:
        months: Количество месяцев для хранения (по умолчанию 2).
    """
    logger.info(
        "Starting task: cleanup_old_requests",
        months=months,
    )

    try:
        async with db_helper.async_session_maker() as session:
            dao = ShiftRequestsDAO(session=session)
            service = ShiftRequestsService(dao=dao)

            deleted_count = await service.cleanup_old_requests(months=months)

            logger.info(
                "Task completed: cleanup_old_requests",
                deleted_count=deleted_count,
                months=months,
                timestamp=datetime.now().isoformat(),
            )
    except Exception as e:
        logger.error(
            "Task failed: cleanup_old_requests",
            error=str(e),
            timestamp=datetime.now().isoformat(),
        )
        raise


def setup_scheduler() -> AsyncIOScheduler:
    """
    Настройка и запуск планировщика задач.

    Returns:
        Настроенный планировщик.
    """
    scheduler = AsyncIOScheduler()

    # Отмена просроченных pending запросов - каждые 5 минут
    scheduler.add_job(
        cancel_expired_pending_requests,
        trigger=CronTrigger(minute="*/5"),
        id="cancel_expired_pending_requests",
        name="Cancel expired pending shift requests",
        replace_existing=True,
    )

    # Очистка старых запросов - каждый день в 03:00
    scheduler.add_job(
        cleanup_old_requests,
        trigger=CronTrigger(hour=3, minute=0),
        id="cleanup_old_requests",
        name="Cleanup old shift requests (older than 2 months)",
        replace_existing=True,
        kwargs={"months": 2},
    )

    return scheduler


# Глобальный экземпляр планировщика
_scheduler: AsyncIOScheduler | None = None


def get_scheduler() -> AsyncIOScheduler:
    """Получить глобальный экземпляр планировщика."""
    global _scheduler
    if _scheduler is None:
        _scheduler = setup_scheduler()
    return _scheduler


def start_scheduler() -> None:
    """Запустить планировщик."""
    scheduler = get_scheduler()
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started")


def stop_scheduler() -> None:
    """Остановить планировщик."""
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        _scheduler.shutdown()
        logger.info("Scheduler stopped")
        _scheduler = None


async def run_task_manually(task_name: str, **kwargs) -> dict:
    """
    Запустить задачу вручную.

    Args:
        task_name: Имя задачи ('cancel_expired' или 'cleanup_old').
        **kwargs: Дополнительные аргументы для задачи.

    Returns:
        Результат выполнения задачи.
    """
    if task_name == "cancel_expired":
        await cancel_expired_pending_requests()
        return {"status": "completed", "task": "cancel_expired_pending_requests"}

    elif task_name == "cleanup_old":
        months = kwargs.get("months", 2)
        await cleanup_old_requests(months=months)
        return {"status": "completed", "task": "cleanup_old_requests", "months": months}

    else:
        return {"status": "error", "message": f"Unknown task: {task_name}"}
