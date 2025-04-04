import json
from datetime import datetime

import aio_pika

class RedisCacheRepository:
    def __init__(self, client):
        self.client = client

    async def add_one(self, message):
        event = json.loads(message.body.decode())
        print(event)
        deadline = datetime.fromisoformat(event["deadline"])
        ttl_seconds = (deadline - datetime.utcnow()).total_seconds()
        
        if ttl_seconds <= 0:
            return 
        key = f"event:{event['id']}"
        await self.client.set(key, json.dumps(event, ensure_ascii=False), ex=int(ttl_seconds))

    async def get_all(self):
        keys = await self.client.keys("event:*")
        events = {}
        for key in keys:
            data = await self.client.get(key)
            event_id = key.split(":")[-1]
            events[event_id] = json.loads(data) if data else None
        return events
