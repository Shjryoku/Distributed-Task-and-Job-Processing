import asyncio
import time
from core.worker.registry.registry import Registry
from core.worker.core.executor import get_next_task, complete_task, fail_task, update_heartbeat
from core.utils import logger as worker_logger
from core.utils.metrics import tasks_failed, task_duration, tasks_completed

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
                worker_logger.info(f"Got task: {task.name}\nWith id: {task.id}\nWorker id: {self.worker_id}")
                try:
                    handler_cls = self.reg.get(task.name)
                    handler = handler_cls()
                    heartbeat = asyncio.create_task(self._heartbeat_loop(task.id))
                    start = time.time()
                    try:
                        await handler.run(task.payload)
                    finally:
                        heartbeat.cancel()
                    
                    duration = time.time() - start
                    task_duration.labels(task_name=task.name).observe(duration)
                    tasks_completed.labels(task_name=task.name).inc()

                    await complete_task(task.id)
                    worker_logger.info(f"Task: {task.name}\nWith id: {task.id} completed\nWorker id: {self.worker_id}")
                except Exception as e:
                    tasks_failed.labels(task_name=task.name).inc()
                    worker_logger.error(f"Task: {task.name}\nWith id: {task.id}\nFailed: {e}\nWorker id: {self.worker_id}")
                    await fail_task(task.id)

    async def _heartbeat_loop(self, task_id, interval = 10):
        while True:
            await update_heartbeat(task_id)
            await asyncio.sleep(interval)