from fastapi import APIRouter, UploadFile, File, status, HTTPException
from datetime import date
from typing import List
import pandas as pd

from schemas import IssuancePlanPerformance, GatherPlanPerformance, Success
from crud import plan_exists, insert_plans, get_plans, get_dictionary_id, get_credits_body, get_payments_sum_by_date
from models import Plan
from helpers.types import to_date

plans_router = APIRouter()

@plans_router.post('/plans_insert')
async def post_plans(file: UploadFile = File(...)) -> Success:
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='File format must be .xlsx')
    
    df = pd.read_excel(await file.read(), converters={0: lambda x: x.date(), 1: str, 2: float})

    plans: List[ dict[str, date | str | float ] ] = []
    for row in df.itertuples():
        plan_date: date = row[1]
        plan_name: str = row[2]
        plan_sum: float = row[3]
        plans.append( { 'period': plan_date, 'name': plan_name, 'sum': plan_sum })

    plan_models: List[Plan] = []
    for plan in plans:
        plan_period, plan_name, plan_sum = plan.values()
        
        if plan_period.day != 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid period. Must be 1 day of month')
        
        if pd.isna(plan_sum):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Invalid plan sum')

        category_id = await get_dictionary_id(plan_name)    
        if not category_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'No such category \'{plan_name}\'')
        
        if await plan_exists(plan_period, category_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'The plan with period {plan_period} and category \'{plan_name}\' already exists in database')
        
        plan_models.append(Plan(period=plan_period, sum=plan_sum, category_id=category_id))

    plan_ids = await insert_plans(plan_models)

    return Success(values=plan_ids)


@plans_router.get('/plans_performance')
async def get_plans_performance(year: int, month: int, day: int) -> List[IssuancePlanPerformance | GatherPlanPerformance]:
    try:
        for_date = date(year, month, day)
    except ValueError as ex:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(ex))
    plans_performance = []
    for plan in  await get_plans(for_date):
        if plan.category.lower() == 'видача':
            issuance_sum = await get_credits_body(plan.period, for_date)
            complete_percent = issuance_sum / plan.sum  * 100
            plan_performance = IssuancePlanPerformance(month=for_date.month, category=plan.category, sum=plan.sum, given_sum=issuance_sum, complete_percent=complete_percent)
        elif plan.category.lower() == 'збір':
            payments_sum = await get_payments_sum_by_date(plan.period, for_date)
            complete_percent = payments_sum / plan.sum  * 100
            plan_performance = GatherPlanPerformance(month=for_date.month, category=plan.category, sum=plan.sum, gathered_sum=payments_sum, complete_percent=complete_percent)
        else:
            continue
        plans_performance.append(plan_performance)
    return plans_performance

