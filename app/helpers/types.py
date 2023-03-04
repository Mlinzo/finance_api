from datetime import datetime, date
from typing import Any

def to_date(x: str) -> date:
    return datetime.strptime(x, '%d.%m.%Y').date()

def to_safe_date(x: str) -> date | None:
    return to_date(x) if x else None
