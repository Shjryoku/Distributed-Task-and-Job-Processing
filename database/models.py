import uuid
import datetime
import enum
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func
from sqlalchemy import Enum as SQLEnum

class Status(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"
    DEAD = "dead"
    DONE = "done"
    CANCELLED = "cancelled"
    SCHEDULED = "scheduled"

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()

    payload: Mapped[dict] = mapped_column(JSONB, default={}, server_default='{}')
    status: Mapped[Status] = mapped_column(SQLEnum(Status, native_enum=True), default=Status.PENDING)
    priority: Mapped[int] = mapped_column()

    retry_attempts: Mapped[int] = mapped_column(default=0)
    retry_limit: Mapped[int] = mapped_column(default=3)

    timeout_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_heartbeat: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    worker_id: Mapped[Optional[str]] = mapped_column(nullable=True)

    idempotency_key: Mapped[str] = mapped_column(unique=True, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    scheduled_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)