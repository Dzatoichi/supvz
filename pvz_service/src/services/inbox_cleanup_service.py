from src.dao.inboxDAO import InboxEventsDAO
from src.settings.config import settings


class InboxCleanupService:
    def __init__(self, inbox_repo: InboxEventsDAO):
        self.inbox_repo = inbox_repo

    async def cleanup(self, batch_size: int = 1000) -> int:
        """
        Удаляет устаревшие inbox-события.
        """
        retention = settings.inbox_retention_period

        # TODO: logs

        try:
            deleted_count = await self.inbox_repo.delete_old_events_batched(
                retention_period=retention,
                batch_size=batch_size,
            )

            return deleted_count

        except Exception:
            raise
