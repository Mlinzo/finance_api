from typing import Generator
from sqlalchemy import select, func
from database import DBSession
from models import Credit
from datetime import date
from dateutil.relativedelta import relativedelta

async def get_credits(user_id: int) -> Generator[Credit, None, None]:
    qs = select(Credit).where(Credit.user_id == user_id)
    async with DBSession() as session:
        return (row[0] for row in (await session.execute(qs)).all())


async def get_credits_body(_from: date, _to: date) -> float:
    qs = select(func.sum(Credit.body).label('issuance_sum')).where( (Credit.issuance_date >= _from) & (Credit.issuance_date <= _to) )
    async with DBSession() as session:
        issuance_sum =  (await session.execute(qs)).one_or_none()[0]
        return issuance_sum if not issuance_sum is None else 0


async def get_issuance_sum_for_month(year: int, month: int) -> float:
    down_date = date(year, month, 1)
    up_date = down_date + relativedelta(months=1)
    qs = select(func.sum(Credit.body)).where( (Credit.issuance_date >= down_date) & (Credit.issuance_date < up_date) )
    async with DBSession() as session:
        issuance_sum = (await session.execute(qs)).one_or_none()[0]
        return issuance_sum if not issuance_sum is None else 0


async def get_issuance_count(year: int, month: int) -> int:
    down_date = date(year, month, 1)
    up_date = down_date + relativedelta(months=1)
    qs = select(func.count(Credit.id)).where( (Credit.issuance_date >= down_date) & (Credit.issuance_date < up_date) )
    async with DBSession() as session:
        issuance_count = (await session.execute(qs)).one_or_none()[0]
        return issuance_count if not issuance_count is None else 0


async def get_year_issuance_sum(year: int) -> float:
    down_date = date(year, 1, 1)
    up_date = down_date + relativedelta(years=1)
    qs = select(func.sum(Credit.body)).where( (Credit.issuance_date >= down_date) & (Credit.issuance_date < up_date) )
    async with DBSession() as session:
        issuance_sum = (await session.execute(qs)).one_or_none()[0]
        return issuance_sum if not issuance_sum is None else 0