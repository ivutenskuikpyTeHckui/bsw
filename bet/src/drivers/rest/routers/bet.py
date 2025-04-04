from typing import Annotated

from fastapi import APIRouter, Depends

from src.drivers.rest.dependencies import bet_service, get_redis_repository
from src.drivers.rest.schemas.bet import BetSchemaAdd
from src.use_cases.bet_service import BetService
from src.adapters.redis_cache.repository import RedisCacheRepository



router = APIRouter(
    tags=["Bets"],
)


@router.get("/bets")
async def get_all(
    bet_service: Annotated[BetService, Depends(bet_service)],
):
    bets = await bet_service.get_all()
    return bets


@router.post("/bet")
async def add_one(
    bet: BetSchemaAdd,
    bet_service: Annotated[BetService, Depends(bet_service)],
):
    bet_id = await bet_service.add_one(bet)
    return bet_id

@router.get("/events")
async def get_events(repository: RedisCacheRepository = Depends(get_redis_repository)):
    events = await repository.get_all()
    return events