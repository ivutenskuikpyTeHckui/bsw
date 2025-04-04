from abc import ABC, abstractmethod

from src.ports.repositories.abs_repository import AbstractRepository


class AbstractUnitOfWork(ABC):
    repository: AbstractRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, traceback):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError
