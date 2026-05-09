import uuid
import datetime

from typing import Optional
from pydantic import BaseModel, ConfigDict
from database.models import Status

class TaskCreate(BaseModel):
    name: str
    priority: int

    payload: dict={}
    idempotency_key: Optional[str] = None
    retry_limit: int = 3

    timeout_seconds: int

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    priority: Optional[int] = None

    payload: Optional[dict] = None
    status: Optional[Status] = None

    retry_limit: Optional[int] = None
    timeout_at: Optional[datetime.datetime] = None


class TaskResponse(BaseModel):
    id: uuid.UUID

    name: str
    payload: dict

    status: Status
    priority: int

    retry_attempts: int
    retry_limit: int

    timeout_at: Optional[datetime.datetime]
    last_heartbeat: Optional[datetime.datetime]
    worker_id: Optional[str]

    idempotency_key: Optional[str]

    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class WorkerAssign(BaseModel):
    worker_id: str