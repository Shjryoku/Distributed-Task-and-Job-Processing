from core.worker.registry.decorators import register
from core.worker.registry.types import TaskType
from core.worker.handlers.base import BaseHandler

@register(task_type=TaskType.SEND_EMAIL)
class EmailHandler(BaseHandler):
    name = "send_email"

    async def handle(self, payload):
        return payload["email"]