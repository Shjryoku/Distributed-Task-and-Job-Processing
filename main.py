import uvicorn
import asyncio
import selectors
import subprocess
import sys
import platform
from config.settings import settings
from core.services.reaper import Reaper
from core.worker.core.worker import Worker
from core.worker.registry import registry
from core.utils.scheduler import Scheduler

def loop_factory():
    return asyncio.SelectorEventLoop(selectors.SelectSelector())

async def main():
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        check=True
    )

    worker = Worker(worker_id="worker_1", timeout_sec=300, reg=registry)
    reaper = Reaper(interval=10)
    scheduler = Scheduler(interval=5)

    server = uvicorn.Server(uvicorn.Config(
        "core.api.router:app",
        host="0.0.0.0",
        port=settings.port
    ))

    await asyncio.gather(
        server.serve(),
        worker.run(), 
        reaper.run(),
        scheduler.run()
    )


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio._WindowsSelectorEventLoopPolicy())
    asyncio.run(main())