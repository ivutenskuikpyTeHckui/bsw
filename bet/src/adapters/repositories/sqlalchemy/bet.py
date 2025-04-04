from src.adapters.repositories.sqlalchemy.base_repository import SQLAlchemyRepository
from src.domain.entity import Bet


class BetRepository(SQLAlchemyRepository):
    model = Bet
