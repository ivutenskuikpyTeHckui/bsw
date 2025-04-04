import asyncio

import random

from datetime import datetime, timedelta

from sqlalchemy import delete


from src.adapters.database.config import async_session_maker
from src.adapters.messaging.producer import RabbitMQProducer
from src.domain.entity import EventStatus, Event, EventName
from src.drivers.rest.schemas.event import EventSchemaAdd


async def create_events():
    """
    Функция создания рандомных событий 
    """
    async with async_session_maker() as session:
        for _ in range(5):
            event = EventSchemaAdd(
                name=random.choice(EventName),
                coefficient=round(random.uniform(1.00, 7.50), 2),
                deadline=datetime.utcnow() + timedelta(seconds=random.randint(25, 30)),
                status=EventStatus.NOT_PLAY
            )

            event_data = event.model_dump()
            instance = Event(**event_data)
            session.add(instance)
            await session.commit()
            event_data["id"] = instance.id

            delay = (event.deadline - datetime.utcnow()).total_seconds()
            asyncio.create_task(update_event_status(instance.id, delay))
            print(event_data)
            await RabbitMQProducer.publish_event(event_data)


async def delete_events():
    async with async_session_maker() as session:
        await session.execute(delete(Event))
        await session.commit()
        

async def update_event_status(event_id: int, delay: int):
    updated_event = {}
    await asyncio.sleep(delay)
    async with async_session_maker() as session:
        event = await session.get(Event, event_id)
        event.status = random.choice([EventStatus.WON_FIRST, EventStatus.WON_SECOND])
        await session.commit()
        updated_event["id"] = event_id
        updated_event["status"] = event.status
        await RabbitMQProducer.publish_updated_event(updated_event)    
