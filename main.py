import uvicorn
import asyncio
import selectors
from config.settings import settings
from core.services.reaper import Reaper
from core.worker.core.worker import Worker
from core.worker.registry import registry
from core.utils.scheduler import Scheduler
import core.worker.handlers.email

def loop_factory():
    return asyncio.SelectorEventLoop(selectors.SelectSelector())

async def main():
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
    asyncio.run(
        main(),
        loop_factory=loop_factory
    )