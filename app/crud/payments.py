from sqlalchemy import select, func
from database import DBSession
from datetime import date
from typing import Generator
from models import Payment
from dateutil.relativedelta import relativedelta

async def get_payments_sum(credit_id: int) -> float:
    qs = select(func.sum(Payment.sum).label('credit_sum')).where(Payment.credit_id == credit_id)
    async with DBSession() as session:
        return (await session.execute(qs)).one().credit_sum 
    
async def get_payments_sum_by_date(_from: date, _to: date) -> float:
    qs = select(func.sum(Payment.sum).label('payment_sum')).where( (Payment.payment_date >= _from) & (Payment.payment_date <= _to) )
    async with DBSession() as session:
        payments_sum =  (await session.execute(qs)).one_or_none()[0]
        return payments_sum if not payments_sum is None else 0
    
    
async def get_payments_sum_for_month(year: int, month: int) -> float:
    down_date = date(year, month, 1)
    up_date = down_date + relativedelta(months=1)
    qs = select(func.sum(Payment.sum)).where( (Payment.payment_date >= down_date) & (Payment.payment_date < up_date) )
    async with DBSession() as session:
        result = (await session.execute(qs)).one_or_none()[0]
        return result if not result is None else 0


async def get_payments_count(year: int, month: int) -> int:
    down_date = date(year, month, 1)
    up_date = down_date + relativedelta(months=1)
    qs = select(func.count(Payment.id)).where( (Payment.payment_date >= down_date) & (Payment.payment_date < up_date) )
    async with DBSession() as session:
        result = (await session.execute(qs)).one_or_none()[0]
        return result if not result is None else 0    


async def get_year_payments_sum(year: int) -> float:
    down_date = date(year, 1, 1)
    up_date = down_date + relativedelta(years=1)
    qs = select(func.sum(Payment.sum)).where( (Payment.payment_date >= down_date) & (Payment.payment_date < up_date) )
    async with DBSession() as session:
        result = (await session.execute(qs)).one_or_none()[0]
        return result if not result is None else 0