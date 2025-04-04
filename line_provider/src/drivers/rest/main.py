from fastapi import FastAPI

from src.drivers.rest.routers.event import router as router_event
from src.domain.scheduler import create_events, delete_events

app = FastAPI(title="Events")

@app.on_event("startup")
async def startup_event():
    await create_events()

@app.on_event("shutdown")
async def shutdown_event():
    await delete_events()

app.include_router(router_event)