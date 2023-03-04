from pydantic import BaseModel, Field
from datetime import date

class UserCredit(BaseModel):
    issuance_date: date
    accrued_interest: float
    issuance_sum: float

class UserCreditClose(UserCredit):
    actual_return_date: date
    payments_sum: float
    credit_closed: bool = Field(default=True)

class UserCreditOpen(UserCredit):
    return_date: date
    overdue_days: int = Field(gt=0)
    payments_sum_body: float
    payments_sum_percent: float
    credit_closed: bool = Field(default=False)
