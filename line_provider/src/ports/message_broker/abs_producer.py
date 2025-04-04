from abc import ABC, abstractmethod
from typing import Dict

class EventProducer(ABC):
    @abstractmethod
    async def publish_event(event: Dict) -> None:
        pass
