import asyncio
from core.worker.registry.registry import Registry
from core.worker.core.executor import get_next_task, complete_task, fail_task, update_heartbeat

class Worker:
    def __init__(
            self, 
            worker_id: str,
            timeout_sec: int,
            reg: Registry
        ):
        self.worker_id = worker_id
        self.timeout_sec = timeout_sec
        self.reg = reg

    async def run(self):
        while True:
            task = await get_next_task(self.worker_id, self.timeout_sec)
            if task is None:
                await asyncio.sleep(5)
            else:
                try:
                    handler_cls = self.reg.get(task.name)
                    handler = handler_cls()
                    heartbeat = asyncio.create_task(self._heartbeat_loop(task.id))
                    try:
                        await handler.run(task.payload)
                    finally:
                        heartbeat.cancel()
                    await complete_task(task.id)
                except Exception:
                    await fail_task(task.id)

    async def _heartbeat_loop(self, task_id, interval = 10):
        while True:
            await update_heartbeat(task_id)
            await asyncio.sleep(interval)