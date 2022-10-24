"""
Module contains main application
"""

import fastapi

from .routes import (
    router_v1
)
from . import database


URL_PREFIX_BASE = "/api/v{}"


main_app = fastapi.FastAPI()

app_v1 = fastapi.FastAPI()
app_v1.include_router(router_v1)

main_app.mount(URL_PREFIX_BASE.format(1), app_v1)

@main_app.on_event("startup")
async def startup_callback():
    await database.init()

@main_app.on_event("shutdown")
async def shutdown_callback():
    await database.deinit()
