import aio_pika
import json

from enum import Enum
from datetime import datetime

from src.adapters.messaging.config import get_amqp_url
from src.ports.message_broker.abs_producer import EventProducer


class RabbitMQProducer(EventProducer):
    @staticmethod
    async def publish_event(event: dict) -> None:
        connection = await aio_pika.connect_robust(get_amqp_url())
        
        async with connection:
            channel = await connection.channel()

            exchange = await channel.declare_exchange("events", aio_pika.ExchangeType.FANOUT)
                
            message_body = await message_serializer(event)
            
            message = aio_pika.Message(body=message_body)

            await exchange.publish(message, routing_key="")

    @staticmethod
    async def publish_updated_event(updated_event: dict):
        connection = await aio_pika.connect_robust(get_amqp_url())

        async with connection:
            channel = await connection.channel()

            exchange = await channel.declare_exchange("updated_events", aio_pika.ExchangeType.FANOUT)

            message_body = await message_serializer(updated_event)

            message = aio_pika.Message(body=message_body)

            await exchange.publish(message, routing_key="")


async def message_serializer(event: dict):
    """
    Преобразование в сереализуемый объект 
    """
    serialized_message = json.dumps(event, default=default_serializer, ensure_ascii=False).encode()
    return serialized_message


def default_serializer(obj):
    """
    Функция для сереализации полей с типами: datetime, Enum
    """
    if isinstance(obj, (datetime)):
        return obj.isoformat()
    elif isinstance(obj, Enum):
        return obj.value
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    else:
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")