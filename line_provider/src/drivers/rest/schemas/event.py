from datetime import datetime

from pydantic import BaseModel

from src.domain.entity import EventStatus

class EventSchemaBase(BaseModel):
    pass


class EventSchemaAdd(EventSchemaBase):
    name: str
    coefficient: float
    deadline: datetime
    status: EventStatus = EventStatus.NOT_PLAY


class EventSchemaEdit(EventSchemaBase):
    id: int
    name: str | None = None
    coefficient: float | None = None
    deadline: datetime | None = None
    status: EventStatus | None = None
