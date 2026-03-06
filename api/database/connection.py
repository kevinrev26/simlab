import os
from sqlalchemy.ext.asyncio import ( create_async_engine, AsyncSession )
from sqlalchemy.orm import sessionmaker

host = os.getenv("POSTGRES_HOSTNAME", "localhost")
port = os.getenv("POSTGRES_PORT", "5432")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD", "pazzword")
database_name = os.getenv("POSTGRES_DB", "simlab_db")

DATABASE_URL = (
    f'postgresql+asyncpg://{user}:{password}'
    f'@{host}:{port}/{database_name}'
)

def get_engine():
    return create_async_engine(
        DATABASE_URL, echo=True
    )

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=get_engine(),
    class_=AsyncSession
)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
