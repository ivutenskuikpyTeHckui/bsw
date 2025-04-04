from sqlalchemy.ext.asyncio import AsyncSession

from src.ports.unit_of_work.uow import AbstractUnitOfWork
from src.adapters.repositories.sqlalchemy.bet import BetRepository


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.repository = BetRepository(self.session)
        return self

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()