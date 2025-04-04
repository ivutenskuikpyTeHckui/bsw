from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete 

from src.ports.repositories.abs_repository import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        instance = self.model(**data)
        self.session.add(instance)

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def edit_one(self, data: dict):
        existing_instance = await self.session.get(self.model, data["id"])
        if not existing_instance:
            return None
        
        for name, value in data.items():
            setattr(existing_instance, name, value)

        return existing_instance.id
    
    async def get_all_ongoing_events(self):
        """
        Получить все текущие события из базы данных.

        Этот метод выполняет запрос для выбора всех записей из модели,
        где статус равен "NOT_PLAY".
        """
        result = await self.session.execute(select(self.model).where(self.model.status == "NOT_PLAY"))
        return result.scalars().all()

    async def delete_all(self):
        await self.session.execute(delete(self.model))
        return {"message": "All events deleted"}