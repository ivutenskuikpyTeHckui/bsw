from src.drivers.rest.schemas.event import EventSchemaAdd

from src.ports.unit_of_work.uow import AbstractUnitOfWork


class EventService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def add_one(self, event: EventSchemaAdd):
        event_dict = event.model_dump()
        async with self.uow as uow:
            event_id = await uow.repository.add_one(event_dict)
            return event_id
        
    async def get_all(self):
        async with self.uow as uow:
            events = await uow.repository.get_all()
            return events
        
    async def edit_one(self, event: EventSchemaAdd):
         event_dict = event.model_dump(exclude_unset=True)
         async with self.uow as uow:
            event_id = await uow.repository.edit_one(event_dict)
            return event_id
         
    async def get_all_ongoing_events(self):
        async with self.uow as uow:
            events = await uow.repository.get_all_ongoing_events()
            return events
        
    async def delete_all(self):
        async with self.uow as uow:
            events = await uow.repository.delete_all()
            return events