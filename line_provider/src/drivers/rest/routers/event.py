import asyncio

from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks

from src.drivers.rest.dependencies import get_event_service
from src.drivers.rest.schemas.event import EventSchemaAdd, EventSchemaEdit
from src.use_cases.event_service import EventService



router = APIRouter(
    tags=["Events"],
    prefix="/events",
)


@router.get("/")
async def get_all(
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    event = await event_service.get_all()
    return event


@router.get("/ongoing")
async def get_all_ongoing_events(
    event_service: Annotated[EventService, Depends(get_event_service)]
):
    events = await event_service.get_all_ongoing_events()
    return events


@router.post("/")
async def add_one(
    event: EventSchemaAdd,
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    event = await event_service.add_one(event)
    return event


@router.patch("/")
async def edit_one(
    event: EventSchemaEdit,
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    event = await event_service.edit_one(event)
    return event


@router.delete("/")
async def delete_all(
    event_service: Annotated[EventService, Depends(get_event_service)],
):
    event = await event_service.delete_all()
    return event
