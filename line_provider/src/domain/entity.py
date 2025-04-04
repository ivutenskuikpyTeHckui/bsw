from enum import Enum
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PGENUM

from src.adapters.database.config import Base


class EventStatus(Enum):
    NOT_PLAY = "Незавершённое"
    WON_FIRST = "Завершено победой первой команды" 
    WON_SECOND = "Завершено победой второй команды" 


EventName = [
    "Россия-Украина",
    "США-Канада",
    "Франция-Германия",
    "Бразилия-Аргентина",
    "Япония-Южная Корея",
    "Италия-Испания",
    "Англия-Португалия",
    "Китай-Индия",
    "Мексика-Чили",
    "Австралия-Новая Зеландия",
]


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    coefficient: Mapped[float] = mapped_column()
    deadline: Mapped[datetime] = mapped_column()
    status: Mapped[EventStatus] = mapped_column(
        PGENUM(EventStatus, name = "event_status", create_type = True),
        server_default=text("'NOT_PLAY'"),
    )