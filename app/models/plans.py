from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from database import Base
from datetime import date
from models import Dictionary

class Plan(Base):
    __tablename__ = 'plans'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    period: Mapped[date] = Column(Date)
    sum: Mapped[float] = Column(Float)
    category_id: Mapped[int] = Column(Integer, ForeignKey(Dictionary.id))
    
    category: Mapped[Dictionary] = relationship(Dictionary, foreign_keys='Plan.category_id')