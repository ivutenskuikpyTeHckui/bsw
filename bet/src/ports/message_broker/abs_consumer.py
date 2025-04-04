from abc import ABC, abstractmethod


class EventConsumer(ABC):
    @abstractmethod
    async def receive_event(self) -> None:
        pass
