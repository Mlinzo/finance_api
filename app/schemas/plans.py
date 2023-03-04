from pydantic import BaseModel
from datetime import date

class PlanView(BaseModel):
    id: int
    period: date
    sum: float
    category: str
    