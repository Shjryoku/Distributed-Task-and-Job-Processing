from abc import ABC, abstractmethod

class BaseHandler(ABC):
    name: str
    timeout: int = 30
    max_retries: int = 3

    async def validate(self, payload: dict) -> None:
        """Validation hook"""
        pass

    @abstractmethod
    async def handle(self, payload: dict) -> None:
        pass

    async def run(self, payload: dict) -> None:
        """Wrapper around execution"""
        await self.validate(payload)
        return await self.handle(payload) 