from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.orm import declarative_base
from helpers.filesystem import get_env

DATABASE_URL = get_env('DATABASE_URL')

if not DATABASE_URL:
    print('Please provide database connection url in .env file using following format: "mysql+aiomysql://{user}:{password}@{host}:{port}/{database}"')
    exit()

engine = create_async_engine(DATABASE_URL)
DBSession = async_sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()