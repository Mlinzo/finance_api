from fastapi import APIRouter
from typing import List
from datetime import date
import asyncio

from schemas import UserCreditClose, UserCreditOpen, MonthPerformance
from crud import get_credits, get_payments_sum, get_plan_sum, get_issuance_sum_for_month, get_issuance_count, get_payments_sum_for_month, get_payments_count, get_year_payments_sum, get_year_issuance_sum
from helpers.functions import calc_percent
#! get_plans_by_year, get_credits_by_year, get_payments_by_year

credits_router = APIRouter()

@credits_router.get('/user_credits/{user_id}')
async def get_user_credits(user_id: int) -> List[UserCreditClose | UserCreditOpen]:
    credits = await get_credits(user_id)
    user_credits = []
    for credit in credits:
        payments_sum = await get_payments_sum(credit.id)
        user_credit = UserCreditClose(
            issuance_date=credit.issuance_date,
            actual_return_date=credit.actual_return_date,
            issuance_sum=credit.body,
            accrued_interest=credit.accrued_interest,
            payments_sum=payments_sum
        ) if credit.actual_return_date else UserCreditOpen(
            issuance_date=credit.issuance_date,
            return_date=credit.return_date,
            overdue_days=(date.today()-credit.return_date).days,
            issuance_sum=credit.body,
            accrued_interest=credit.accrued_interest,
            payments_sum_body=payments_sum,
            payments_sum_percent=credit.percent-payments_sum
        )
        user_credits.append(user_credit)
    return user_credits

@credits_router.get('/year_performance/{year}')
async def get_year_performance(year: int) -> List[MonthPerformance]:
    year_performance = []
    for i in range(1, 13):
        month = i
        issuance_count, plan_issuance_sum, issuance_sum, \
        payments_count, plan_gather_sum, payments_sum, \
        year_issuance_sum, year_payments_sum = await asyncio.gather(*[
            get_issuance_count(year, month), get_plan_sum(year, month, 'видача'), get_issuance_sum_for_month(year, month),
            get_payments_count(year, month), get_plan_sum(year, month, 'збір'), get_payments_sum_for_month(year, month),
            get_year_issuance_sum(year), get_year_payments_sum(year)
        ])
        month_performance = MonthPerformance(
            month=month, year=year,
            issuance_count=issuance_count, plan_issuance_sum=plan_issuance_sum,
            issuance_sum=issuance_sum, issuance_complete_percent=calc_percent(issuance_sum, plan_issuance_sum),
            payments_count=payments_count, plan_gather_sum=plan_gather_sum,
            payments_sum=payments_sum, gather_complete_percent=calc_percent(payments_sum, plan_gather_sum),
            issuance_sum_percent=calc_percent(issuance_sum, year_issuance_sum), gather_sum_percent=calc_percent(payments_sum, year_payments_sum)
        )
        year_performance.append(month_performance)
    return year_performance