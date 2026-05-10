import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from core.api.router import app
from database.connection import AsyncSessionLocal
from sqlalchemy import delete
from database.models import Task

asyncio.set_event_loop_policy(
    asyncio.WindowsSelectorEventLoopPolicy()
)

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.fixture(autouse=True)
async def clear_tasks():
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Task))
        await session.commit()
