from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from database import Base
from datetime import date
from models import User

class Credit(Base):
    __tablename__ = 'credits'
    
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey(User.id), primary_key=True)
    issuance_date: Mapped[date] = Column(Date,nullable=False)
    return_date: Mapped[date] = Column(Date, nullable=False)
    actual_return_date: Mapped[date] = Column(Date, nullable=True)
    body: Mapped[float] = Column(Float, nullable=False)
    accrued_interest: Mapped[float] = Column(Float, nullable=False)
    
    user: Mapped[User] = relationship(User, foreign_keys='Credit.user_id')
