from typing import Type
from core.worker.handlers.base import BaseHandler
from core.worker.registry.types import TaskType

class Registry:
    def __init__(self):
        self._handlers: dict[TaskType, Type[BaseHandler]] = {}

    def register(self, task_type: TaskType, handler: Type[BaseHandler]) -> None:
        self._handlers[task_type] = handler
    
    def get(self, task_type: TaskType) -> Type[BaseHandler]:
        handler = self._handlers.get(task_type)

        if not handler:
            raise ValueError(f"No handlers registered for {task_type}")
        return handler

registry = Registry()