from datetime import date
from sqlalchemy import select
from database import DBSession
from typing import Iterable, List, Generator
from schemas import PlanView
from models import Plan, Dictionary

async def plan_exists(period: date, category_id: int) -> bool:
    qs = select(Plan.id).where((Plan.period == period) & (Plan.category_id == category_id))
    async with DBSession() as session:
        return bool( (await session.execute(qs)).one_or_none() )


async def insert_plans(plans: Iterable[Plan]) -> List[int]:
    async with DBSession() as session:
        session.add_all(plans)
        await session.flush()
        ids = [ plan.id for plan in plans ]
        await session.commit()
        return ids


async def get_plans(plan_date: date) -> Generator[PlanView, None, None]:
    target_date = plan_date.replace(day=1)
    qs = select(Plan.id, Plan.period, Plan.sum, Dictionary.name).join(Dictionary, Dictionary.id == Plan.category_id).where(Plan.period == target_date)
    async with DBSession() as session:
        result = (await session.execute(qs)).all()
        if not result: return []
        plan_kwargs = ('id', 'period', 'sum', 'category')
        return ( PlanView( **{key: value for key, value in zip(plan_kwargs, row)} ) for row in result )


async def get_plan_sum(year: int, month: int,  plan_type: str) -> float:
    target_date = date(year, month, 1)
    qs = select(Plan.sum).join(Dictionary, Dictionary.id == Plan.category_id).where( (Plan.period == target_date) & (Dictionary.name == plan_type.lower() ) )
    async with DBSession() as session:
        result = (await session.execute(qs)).one_or_none()
        return result[0] if result else 0