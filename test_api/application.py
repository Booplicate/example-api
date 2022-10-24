"""
Module contains main application
"""

import fastapi

from .routes import (
    router_v1
)


URL_PREFIX_BASE = "/api/v{}"


main_app = fastapi.FastAPI()

app_v1 = fastapi.FastAPI()
app_v1.include_router(router_v1)

main_app.mount(URL_PREFIX_BASE.format(1), app_v1)
