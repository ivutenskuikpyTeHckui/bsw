from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError
    
    @abstractmethod
    async def edit_one(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all_ongoing_events(self):
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all():
        raise NotImplementedError
