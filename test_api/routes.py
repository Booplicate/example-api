"""
Module with the routes for the API
"""

import fastapi

from .models import (
    UserModelIn,
    UserModelOut
)
from . import (
    services
)


router_v1 = fastapi.APIRouter(prefix="/users")


@router_v1.post("", response_model=UserModelOut, status_code=201)
async def create_user(user: UserModelIn):
    return await services.create_user(user.dict())

@router_v1.put("/{identifier}", response_model=UserModelOut)
async def update_user(identifier: int, user: UserModelIn):
    db_data = await services.update_user(identifier, user.dict())
    if db_data is None:
        raise fastapi.HTTPException(404, detail=f"User with id {identifier} not found")

    return db_data

@router_v1.get("/{identifier}", response_model=UserModelOut)
async def get_user(identifier: int):
    db_data = await services.get_user(identifier)
    if db_data is None:
        raise fastapi.HTTPException(404, detail=f"User with id {identifier} not found")

    return db_data
