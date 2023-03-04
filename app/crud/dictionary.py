from sqlalchemy import select
from database import DBSession
from models import Dictionary

async def get_dictionary_id(name: str) -> int | None:
    qs = select(Dictionary.id).where(Dictionary.name == name)
    async with DBSession() as session:
        result = (await session.execute(qs)).one_or_none()
        return result[0] if result else None

