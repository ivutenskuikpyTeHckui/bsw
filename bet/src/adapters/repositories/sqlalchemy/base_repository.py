from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.ports.repositories.abs_repository import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        return instance.id

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
