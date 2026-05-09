from core.worker.registry.registry import registry
from core.worker.registry.types import TaskType

def register(task_type: TaskType):
    def decorator(handler_cls):
        registry.register(task_type, handler_cls)
        return handler_cls
    return decorator