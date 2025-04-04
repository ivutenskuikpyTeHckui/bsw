from typing import Annotated

import redis.asyncio as redis 
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.use_cases.bet_service import BetService
from src.adapters.database.config import get_async_session
from src.adapters.repositories.sqlalchemy.uow import SQLAlchemyUnitOfWork

from src.adapters.redis_cache.repository import RedisCacheRepository


def bet_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    uow = SQLAlchemyUnitOfWork(session)
    return BetService(uow)


def get_redis_repository(request: Request):
    """
    Зависимость, которая возвращает экземпляр репозитория,
    сохранённая в app.state.
    """
    return request.app.state.redis_cache_repository