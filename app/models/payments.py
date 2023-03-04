from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from database import Base
from datetime import date
from models import Dictionary, Credit

class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    sum: Mapped[float] = Column(Float)
    payment_date: Mapped[date] = Column(Date)
    type_id: Mapped[date] = Column(Integer, ForeignKey(Dictionary.id))
    credit_id: Mapped[date] = Column(Integer, ForeignKey(Credit.id))

    type: Mapped[Dictionary] = relationship('Dictionary', foreign_keys='Payment.type_id')
    credit: Mapped[Credit] = relationship('Credit', foreign_keys='Payment.credit_id')