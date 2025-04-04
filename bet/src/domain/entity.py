from enum import Enum

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM as PGENUM

from src.adapters.database.config import Base


class BetStatus(Enum):
    NOT_PLAY = "Ещё не сыграла"
    WON = "Выиграла" 
    LOST = "Проиграла" 


class Bet(Base):
    __tablename__ = "bet"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_event: Mapped[int]
    amount: Mapped[int] = mapped_column()
    status: Mapped[BetStatus] = mapped_column(
        PGENUM(BetStatus, name = "bet_status", create_type = True),
        server_default=text("'NOT_PLAY'"),
    )