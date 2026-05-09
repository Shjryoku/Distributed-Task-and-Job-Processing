import asyncio
import datetime
from database.models import Task, Status
from database.connection import AsyncSessionLocal
from sqlalchemy import select, and_
from core.utils import logger as reaper_logger

class Reaper:
    def __init__(
            self,
            interval: int
        ):
        self.interval = interval

    async def run(self):
        while True:
            async with AsyncSessionLocal() as db:
                async with db.begin():
                    now = datetime.datetime.now(datetime.timezone.utc)
                    stmt = (
                        select(Task)
                        .where(
                            and_(
                                Task.status == Status.RUNNING,
                                Task.timeout_at < now
                                )
                            )
                        .with_for_update(skip_locked=True)
                        .order_by(Task.created_at)
                    )

                    result = await db.execute(stmt)
                    tasks = result.scalars().all()

                    for task in tasks:
                        if task.retry_attempts >= task.retry_limit:
                            task.status = Status.DEAD
                            reaper_logger.info(f"Task: {task.name}\nWith id: {task.id}\nChanged to dead: {task.retry_attempts} is now on limit")
                            continue

                        task.retry_attempts += 1
                        task.status = Status.PENDING

                        task.worker_id = None

                        task.updated_at = now
                        task.timeout_at = None
                        
                        reaper_logger.info(f"Task: {task.name}\nWith id: {task.id}\nReturned to PENDING\nAttempt: {task.retry_attempts}")

            await asyncio.sleep(self.interval)
