from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Mapped
from database import Base
from datetime import date

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    login: Mapped[str] = Column(String(length=255), nullable=False)
    registration_date: Mapped[date] = Column(Date)
