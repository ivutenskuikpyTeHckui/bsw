from src.drivers.rest.schemas.bet import BetSchemaAdd

from src.ports.unit_of_work.uow import AbstractUnitOfWork


class BetService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def add_one(self, bet: BetSchemaAdd):
        bet_dict = bet.model_dump()
        async with self.uow as uow:
            bet_id = await uow.repository.add_one(bet_dict)
            return bet_id
    
    async def get_all(self):
        async with self.uow as uow:
            bets = await uow.repository.get_all()
            return bets
