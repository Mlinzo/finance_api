from pydantic import BaseModel, Field
from typing import List, Any

class Success(BaseModel):
    message: str = Field(default='success')
    values: List[Any] = Field(default_factory =list)