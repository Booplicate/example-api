"""
Module with API models
"""

import datetime

# import pydantic
from pydantic import BaseModel# pylint: disable=no-name-in-module


class _UserModelBase(BaseModel):
    name: str

class UserModelIn(_UserModelBase):
    """
    A model representing user data we request

    Extra requirement:
        password
    """
    password: str

class UserModelOut(_UserModelBase):
    """
    A model representing user data we return

    Extra requirement:
        identifier
        created_at
    """
    identifier: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
