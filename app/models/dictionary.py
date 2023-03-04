from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped
from database import Base


class Dictionary(Base):
    __tablename__ = 'dictionary'
    
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = Column(String(255), unique=True, nullable=False)
