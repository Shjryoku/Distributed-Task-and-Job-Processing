import datetime
import uuid
from database.connection import AsyncSessionLocal
from database.models import Task, Status
from sqlalchemy import select, or_, and_

async def get_next_task(
    worker_id: str,
    timeout_sec: int,
):
    async with AsyncSessionLocal() as db:
        async with db.begin():
            now = datetime.datetime.now(datetime.timezone.utc)
            stmt = (
                select(Task)
                .where(
                    or_(
                        Task.status == Status.PENDING,
                        and_(
                            Task.status == Status.RUNNING,
                            Task.timeout_at < now
                        )))
                .with_for_update(skip_locked=True)
                .order_by(Task.created_at)
                .limit(1)
            )

            result = await db.execute(stmt)
            task = result.scalars().first()

            if not task:
                return None

            if task.retry_attempts < task.retry_limit:
                task.retry_attempts = (task.retry_attempts or 0) + 1
            else:
                task.status = Status.DEAD
                return task

            task.status = Status.RUNNING
            task.worker_id = worker_id

            task.updated_at = now
            task.last_heartbeat = now
            task.timeout_at = now + datetime.timedelta(seconds=timeout_sec)

            return task
        

async def fail_task(
    task_id: uuid.UUID
):
    async with AsyncSessionLocal() as db:
        async with db.begin():
            now = datetime.datetime.now(datetime.timezone.utc)
            task = await db.get(Task, task_id)

            if not task:
                return None
            
            task.status = Status.FAILED
            task.worker_id = None
            task.updated_at = now
            task.timeout_at = now

            return task
            


async def complete_task(
    task_id: uuid.UUID
):
    async with AsyncSessionLocal() as db:
        async with db.begin():
            now = datetime.datetime.now(datetime.timezone.utc)
            task = await db.get(Task, task_id)

            if not task:
                return None
            
            task.status = Status.DONE
            task.worker_id = None
            task.updated_at = now
            task.timeout_at = now

            return task

async def update_heartbeat(
        task_id: uuid.UUID
):
    async with AsyncSessionLocal() as db:
        async with db.begin():
            now = datetime.datetime.now(datetime.timezone.utc)
            task = await db.get(Task, task_id)

            if not task:
                return None
            
            task.last_heartbeat = now
            task.updated_at = now