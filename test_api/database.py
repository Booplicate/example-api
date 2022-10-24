"""
Module with various sql db utils and table definitions
"""

import os

import sqlalchemy
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession
)
from sqlalchemy import (
    select,
    insert,
    update,
    delete,
    Column,
    Integer,
    String,
    DateTime,
    # Table,
    create_engine
)
from sqlalchemy.orm import (
    declarative_base,# DeclarativeBase
    sessionmaker
)


ASYNC_ENGINE_URL_FMT = "postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine: sqlalchemy.ext.asyncio.AsyncEngine|None = None
SessionFactory: AsyncSession|None = None

Base = declarative_base()
metadata = Base.metadata


class User(Base):# type: ignore
    """
    Represents user data
    """
    __tablename__ = "users"

    identifier = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    # __mapper_args__ = {"eager_defaults": True}

    def __repr__(self) -> str:
        return (
            f"User(identifier={self.identifier}, name={self.name}, "
            f"password={self.password}, created_at={self.created_at})"
        )

# users_table: Table = User.__table__


async def init():
    """
    Inits the database
    """
    global engine, SessionFactory

    try:
        db_user = os.environ["POSTGRES_USER"]
        db_password = os.environ["POSTGRES_PASSWORD"]
        db_host = os.environ["PGHOST"]
        db_port = os.environ["PGPORT"]
        db_name = os.environ["POSTGRES_DB"]

    except KeyError as e:
        raise RuntimeError(f"Missing required enviroment variable: {e}") from None

    engine = create_async_engine(
        ASYNC_ENGINE_URL_FMT.format(
            db_user=db_user,
            db_password=db_password,
            db_host=db_host,
            db_port=db_port,
            db_name=db_name
        )
    )

    SessionFactory = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

async def deinit():
    """
    Closes db connection once and for all
    """
    global engine, SessionFactory

    await engine.dispose()
    engine = SessionFactory = None

def new_session(**kwargs) -> AsyncSession:
    """
    Creates a new session to work with the db
    """
    if SessionFactory is None:
        raise RuntimeError("Database hasn't been initialised yet")

    return SessionFactory(**kwargs)
