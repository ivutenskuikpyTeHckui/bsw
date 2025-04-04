from src.adapters.repositories.sqlalchemy.base_repository import SQLAlchemyRepository
from src.domain.entity import Event


class EventRepository(SQLAlchemyRepository):
    model = Event
