from pydantic import BaseModel, Field, validator
from helpers.types import to_date

class PlanPerformance(BaseModel):
    month: int = Field(gt=0, lt=13)
    category: str
    sum: float
    complete_percent: float

class IssuancePlanPerformance(PlanPerformance):
    given_sum: float

class GatherPlanPerformance(PlanPerformance):
    gathered_sum: float

class MonthPerformance(BaseModel):
    month: int
    year: int
    issuance_count: int
    plan_issuance_sum: float
    issuance_sum: float
    issuance_complete_percent: float
    payments_count: int
    plan_gather_sum: float
    payments_sum: float
    gather_complete_percent: float
    issuance_sum_percent: float
    gather_sum_percent: float