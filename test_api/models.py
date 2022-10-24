"""
Module with API models
"""

import datetime

# import pydantic
from pydantic import BaseModel# pylint: disable=no-name-in-module


class _UserModelBase(BaseModel):# pylint: disable=no-member
    name: str

class UserModelIn(_UserModelBase):
    """
    A model representing user data we request

    Extra requirement:
        password
    """
    password: str

    # class Config:
    #     orm_mode = True

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

class UserModel(UserModelIn, UserModelOut):
    """
    A model representing user data we use internally

    Extra requirement:
        password
        identifier
        created_at
    """
    class Config:
        orm_mode = True
