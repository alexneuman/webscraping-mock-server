
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy import inspect

from app.db.base import metadata
from app.models.category import Category
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.environ.get('DATABASE_URL')
print(DATABASE_URL)
connect_args = {'check_same_thread': False} if 'sqlite' in DATABASE_URL.lower() else {}
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_metadata():
    await init_db()
    return SQLModel.metadata

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        # To reflect existing tables, pass the connection:
        await conn.run_sync(lambda sync_conn: SQLModel.metadata.reflect(bind=sync_conn))

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise

async def is_initialized() -> bool:
    """
    Returns True if the database has at least one table, False otherwise.
    """
    async with engine.begin() as conn:
        def check_tables(sync_conn) -> bool:
            inspector = inspect(sync_conn)
            return bool(inspector.get_table_names())

        return await conn.run_sync(check_tables)
