from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.database.config import get_async_session
from src.adapters.messaging.config import get_amqp_url
from src.adapters.messaging.producer import RabbitMQProducer
from src.adapters.repositories.sqlalchemy.uow import SQLAlchemyUnitOfWork
from src.ports.unit_of_work.uow import AbstractUnitOfWork

from src.use_cases.event_service import EventService


def get_event_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    uow = SQLAlchemyUnitOfWork(session)
    return EventService(uow)

def get_broker(amqp_url: Annotated[str, Depends(get_amqp_url)]):
    broker = RabbitMQProducer(amqp_url)
    return broker