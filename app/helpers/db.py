from database import DBSession, Base
from models import User, Dictionary, Credit, Payment, Plan
from sqlalchemy import select,  Table

async def has_data(model: User | Dictionary | Credit | Payment | Plan) -> bool:
    async with DBSession() as session:
        data = await session.execute(select(model).limit(1))
        return bool(data.fetchall())
    