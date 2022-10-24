"""
Modules with different services for the app
"""

import datetime

from .database import (
    select,
    update,
    new_session,
    User
)
from . import encoder
from . import utils


def _preprocess_user_data(user_data: dict):
    """
    Preprocessing user data before adding it
    to the db
    """
    if "password" in user_data:
        user_data["password"] = encoder.hash_string(
            user_data["password"]
        )

def _preprocess_new_user_data(user_data: dict):
    """
    Preprocessing NEW user data before adding it
    to the db
    """
    _preprocess_user_data(user_data)

    if "created_at" not in user_data:
        # NOTE: Unaware dt
        user_data["created_at"] = datetime.datetime.utcnow()


async def create_user(user_data: dict) -> User:
    """
    Creates a new user row in the db
    """
    _preprocess_new_user_data(user_data)

    async with new_session() as sesh:
        db_user = User(**user_data)
        sesh.add(db_user)
        await sesh.commit()

    get_user.clear_key(db_user.identifier)# type: ignore

    return db_user

async def update_user(identifier: int, new_user_data: dict) -> User|None:
    """
    Updates a user row in the db
    """
    _preprocess_user_data(new_user_data)

    async with new_session() as sesh:
        stmt = (
            update(User)
            .where(User.identifier == identifier)
            .values(**new_user_data)
            .returning(User)
        )
        res = await sesh.execute(stmt)
        is_invalid = res.scalar() is None
        # Doesn't exist, abort transaction
        if is_invalid:
            await sesh.rollback()
            return None

        await sesh.commit()

        stmt = select(User).where(User.identifier == identifier)
        res = await sesh.execute(stmt)
        db_user = res.scalar()

    get_user.clear_key(identifier)# type: ignore

    return db_user

@utils.create_async_cache(1024**2)
async def get_user(identifier: int) -> User|None:
    """
    Returns a user from the db
    """
    async with new_session() as sesh:
        db_user = await sesh.get(User, identifier)

    return db_user
