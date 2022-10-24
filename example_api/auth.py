"""
Module implements basic auth support
"""

import secrets

from fastapi import (
    Depends,
    HTTPException
)
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials
)

from . import encoder
from .database import (
    User,
    new_session
)


basic_auth = HTTPBasic()


async def verify_credentials(identifier: int, crdn: HTTPBasicCredentials = Depends(basic_auth)):
    """
    Authorizes a user with the given identifier and credentials
    Throws HTTPException on a failure
    """
    async with new_session() as sesh:
        db_user = await sesh.get(User, identifier)
        if db_user is None:
            raise HTTPException(404, detail=f"Failed to authorize for id {identifier}")

    is_name_valid = secrets.compare_digest(crdn.username, db_user.name)
    is_pw_valid = encoder.verify_string(crdn.password, db_user.password)

    if not is_name_valid or not is_pw_valid:
        raise HTTPException(401, detail="Incorrect username and/or password")
