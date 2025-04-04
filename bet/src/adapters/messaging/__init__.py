import asyncio
import aio_pika
import json
import logging

# Функция-обработчик входящих сообщений
async def on_message(message: aio_pika.IncomingMessage) -> None:
    async with message.process():
        # Десериализуем JSON-сообщение в словарь
        event = json.loads(message.body.decode())
        print("Получено событие:", event)

async def consume_events() -> None:
    # Устанавливаем соединение с RabbitMQ
    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/")
    
    async with connection:
        # Создаем канал
        channel = await connection.channel()
        
        # Ограничиваем количество предварительно получаемых сообщений до 10
        await channel.set_qos(prefetch_count=10)
        
        # Объявляем exchange с тем же именем и типом, что и в publisher
        exchange = await channel.declare_exchange("events", aio_pika.ExchangeType.FANOUT)
        
        # Объявляем очередь для потребителя.
        # Параметр durable=True обеспечивает сохранение очереди между перезапусками,
        # а auto_delete=False (по умолчанию) сохраняет очередь, пока она нужна.
        queue = await channel.declare_queue("events_queue", durable=True)
        
        # Привязываем очередь к exchange.
        # Для FANOUT routing_key не используется.
        await queue.bind(exchange, routing_key="")
        
        logging.info("Ожидание сообщений. Для выхода нажмите CTRL+C")
        
        # Получаем итератор сообщений из очереди
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await on_message(message)
                # Если необходимо, можно добавить условие для завершения цикла
                # например, если событие содержит определённое значение.

if __name__ == "__main__":
    # Запускаем асинхронного потребителя с помощью asyncio.run()
    asyncio.run(consume_events())
