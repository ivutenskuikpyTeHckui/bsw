import json

import aio_pika

from src.adapters.redis_cache.repository import RedisCacheRepository
from src.adapters.messaging.config import get_amqp_url
from src.domain.scheduler_of_updated_events import update_events

                
async def consume_events(repository: RedisCacheRepository) -> None:
    connection = await aio_pika.connect_robust(get_amqp_url(), heartbeat=30)
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        exchange = await channel.declare_exchange("events", aio_pika.ExchangeType.FANOUT)
        queue = await channel.declare_queue("events", durable=True)
        await queue.bind(exchange, routing_key="")
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await repository.add_one(message)


async def consume_updated_events():
    connection = await aio_pika.connect_robust(get_amqp_url())
    async with connection:
        channel = await connection.channel()
        
        await channel.set_qos(prefetch_count=10)
        
        exchange = await channel.declare_exchange("updated_events", aio_pika.ExchangeType.FANOUT)
        
        queue = await channel.declare_queue("updated_events", durable=True)
        
        await queue.bind(exchange, routing_key="")
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await on_message(message)


async def on_message(message: aio_pika.IncomingMessage) -> None:
    async with message.process():
        event = json.loads(message.body.decode())
        await update_events(event)