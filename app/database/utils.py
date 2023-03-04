from database import Base, engine, DBSession
from models import Credit, User, Dictionary, Payment, Plan
from helpers.types import to_date, to_safe_date
from helpers.filesystem import load_data, get_env
from helpers.db import has_data
from logger import db_logger as logger

from typing import Callable, Any

SAMPLE_DATA_DIR = get_env('SAMPLE_DATA_DIR')


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def gen_fill(model: Credit | User | Dictionary | Payment | Plan, columns: tuple[str], converters: tuple[Callable[[str], Any]]) -> Callable[[], None]:
    async def fill():
        if not SAMPLE_DATA_DIR or await has_data(model): return
        data = load_data(SAMPLE_DATA_DIR + '/' + f'{model.__tablename__}.csv', converters)
        kwargs = ({ key: value for key, value in zip(columns, row) if key != 'id'} for row in data)
        rows = (model(**kwargs) for kwargs in kwargs)
        async with DBSession() as session:
            session.add_all(rows)
            await session.commit()
        logger.info(f'{model.__tablename__} table filled')
    return fill


fill_credits = gen_fill(
    model=Credit,
    columns=('id', 'user_id', 'issuance_date', 'return_date', 'actual_return_date', 'body', 'accrued_interest'),
    converters=(int, int, to_date, to_date, to_safe_date, float, float)
)


fill_users = gen_fill(
    model=User,
    columns=('id', 'login', 'registration_date'),
    converters=(int, str, to_date)
)


fill_dictionary = gen_fill(
    model=Dictionary,
    columns=('id', 'name'),
    converters=(int, str)
)


fill_plans = gen_fill(
    model=Plan,
    columns=('id', 'period', 'sum', 'category_id'),
    converters=(int, to_date, float, int)
)


fill_payments = gen_fill(
    model=Payment,
    columns=('id', 'credit_id', 'payment_date', 'type_id', 'sum'),
    converters=(int, int, to_date, int, float)
)


async def fill_db():
    await fill_users()
    await fill_credits()
    await fill_dictionary()
    await fill_plans()
    await fill_payments()
