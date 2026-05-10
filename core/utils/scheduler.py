import asyncio
import datetime
from database.models import Task, Status
from database.connection import AsyncSessionLocal
from sqlalchemy import select, and_
from core.utils import logger as scheduler_logger

class Scheduler:
    def __init__(self, interval: int):
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
                                Task.status == Status.SCHEDULED,
                                Task.scheduled_at <= now
                                )
                            )
                        .with_for_update(skip_locked=True)
                        .order_by(Task.created_at)
                    )

                    result = await db.execute(stmt)
                    tasks = result.scalars().all()

                    for task in tasks:
                        scheduler_logger.info(f"Task: {task.name}\nWith id: {task.id}\nChanged to Pending")
                        task.status = Status.PENDING

            await asyncio.sleep(self.interval)
