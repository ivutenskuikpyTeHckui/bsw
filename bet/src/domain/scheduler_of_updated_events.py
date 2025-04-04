from enum import Enum

from sqlalchemy import select

from src.adapters.database.config import async_session_maker
from src.domain.entity import Bet, BetStatus


class EventStatus(Enum):
    WON_FIRST = "Завершено победой первой команды" 
    WON_SECOND = "Завершено победой второй команды" 
    

async def update_events(event: dict):
    """
    Функция для обновления статусов событий, если на них есть ставки 
    """
    flag = await check_for_victory(event)
    print(flag)
    print(event)
    async with async_session_maker() as session:
        result = await session.execute(select(Bet).where(Bet.id_event == event["id"]))

        bets = result.scalars().all()

        if flag == True:
            for bet in bets:
                bet.status = BetStatus.WON
        elif flag == False:
            for bet in bets:
                bet.status = BetStatus.LOST
    
        await session.commit()


async def check_for_victory(event: dict):
    if event["status"] == EventStatus.WON_FIRST.value:
        return True
    elif event["status"] == EventStatus.WON_SECOND.value:
        return False
