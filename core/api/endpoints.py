import datetime
import uuid
from database.connection import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.api.schemas import TaskCreate, TaskResponse, TaskSchedule, WorkerAssign
from database.models import Task, Status
from sqlalchemy import delete, select, func
from sqlalchemy.exc import IntegrityError
from core.utils.metrics import queue_size

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/next", response_model=TaskResponse, status_code=200)
async def get_next_task(
    worker_id: str,
    timeout_sec: int,
    db:AsyncSession = Depends(get_db)
):
    stmt = (
        select(Task)
        .where(Task.status == Status.PENDING)
        .with_for_update(skip_locked=True)
        .order_by(Task.created_at)
        .limit(1)
    )

    result = await db.execute(stmt)
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = Status.RUNNING
    task.worker_id = worker_id

    now = datetime.datetime.now(datetime.timezone.utc)
    task.updated_at = now
    task.timeout_at = now + datetime.timedelta(seconds=timeout_sec)

    db.add(task)

    await db.commit()
    await db.refresh(task)

    return task
    

@router.post("/schedule", status_code=201)
async def schedule_task(
    task_data: TaskSchedule,
    db: AsyncSession = Depends(get_db)
    ):
    task = Task(
        **task_data.model_dump(),
        status = Status.SCHEDULED
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    return task

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    task = Task(**task_data.model_dump(exclude={"timeout_seconds"}))

    db.add(task)
    
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        stmt = (
            select(Task)
            .where(Task.idempotency_key == task.idempotency_key)
        )
        result = await db.execute(stmt)
        old_task = result.scalars().first()

        await db.refresh(old_task)

        return old_task

    await db.refresh(task)

    return task

@router.delete("/", status_code=204)
async def delete_tasks(
    db: AsyncSession = Depends(get_db)
):
    await db.execute(delete(Task))
    await db.commit()

@router.delete("/{id}", status_code=204)
async def delete_task(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    task = await db.get(Task, id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(task)
    await db.commit()

@router.patch("/{id}/done", response_model=TaskResponse , status_code=200)
async def complete_task(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    task = await db.get(Task, id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = Status.DONE

    db.add(task)

    await db.commit()
    await db.refresh(task)

    return task

@router.patch("/{id}/assign", response_model=TaskResponse, status_code=200)
async def assign_task(
    id: uuid.UUID,
    data: WorkerAssign,
    db: AsyncSession = Depends(get_db)
):
    task = await db.get(Task, id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.worker_id = data.worker_id
    
    db.add(task)

    await db.commit()
    await db.refresh(task)

    return task

@router.patch("/{id}/cancel", status_code=204)
async def cancel_task(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    task = await db.get(Task, id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = Status.CANCELLED

    db.add(task)

    await db.commit()
    await db.refresh(task)

    return task

@router.get("metrics/queue", status_code=200)
async def get_queue_metrics(
    db: AsyncSession = Depends(get_db)
):
    res = await db.execute(
        select(func.count().where(Task.status == Status.PENDING))
    )
    count = res.scalar()
    queue_size.set(count)

    return {"queue_size", count}