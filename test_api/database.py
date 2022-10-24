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


SYNC_ENGINE_URL = "postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
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


def init():
    """
    Inits the database
    """
    global engine, SessionFactory

    try:
        db_user = os.environ["DB_USER"]
        db_password = os.environ["DB_PASSWORD"]
        db_host = os.environ["DB_HOST"]
        db_port = os.environ["DB_PORT"]
        db_name = os.environ["DB_NAME"]

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

    # TODO: perhaps move this to the app callbacks
    _sync_engine = create_engine(
        SYNC_ENGINE_URL.format(
            db_user=db_user,
            db_password=db_password,
            db_host=db_host,
            db_port=db_port,
            db_name=db_name
        ),
        future=True
    )
    metadata.create_all(_sync_engine)

def new_session(**kwargs) -> AsyncSession:
    """
    Creates a new session to work with the db
    """
    if SessionFactory is None:
        raise RuntimeError("Database hasn't been initialised yet")

    return SessionFactory(**kwargs)
