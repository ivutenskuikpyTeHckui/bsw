import asyncio
from fastapi import FastAPI

from src.adapters.redis_cache.config import get_redis_client
from src.adapters.redis_cache.repository import RedisCacheRepository
from src.adapters.messaging.consumer import consume_events, consume_updated_events
from src.drivers.rest.routers.bet import router as router_bet


app = FastAPI(title="Bets")


@app.on_event("startup")
async def startup_event():
    app.state.redis_cache_repository = RedisCacheRepository(get_redis_client())
    asyncio.create_task(consume_events(app.state.redis_cache_repository))
    asyncio.create_task(consume_updated_events())


@app.on_event("shutdown")
async def shutdown_event():
    await get_redis_client().close()


app.include_router(router_bet)