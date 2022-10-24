"""
Modules with util functions and classes
"""

from functools import (
    wraps,
    _make_key as make_key
)
from collections import OrderedDict
from collections.abc import Awaitable
from typing import (
    Callable,
    TypeVar,
    ParamSpec
)


R = TypeVar("R")
P = ParamSpec('P')


def create_async_cache(max_size: int) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """
    Creates a cache for a coro with the specified max size
    """
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """
        Decorator that wraps the function and returns a wrapper around it
        which utilises cache
        """
        cache = OrderedDict()# type: ignore

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """
            Wrapper around a callable which utilises cache
            """
            k = make_key(args, kwargs, False)
            # Check if new key
            if k not in cache:
                # Check if over limit
                if len(cache) > max_size:
                    cache.popitem(last=False)

                cache[k] = await func(*args, **kwargs)

            return cache[k]

        def clear_all():
            """
            Clears cache
            """
            cache.clear()

        def clear_key(key):
            """
            Clears cache for a key
            """
            cache.pop(key, None)

        setattr(wrapper, "__wrapped__", func)
        setattr(wrapper, "__cache__", cache)
        setattr(wrapper, "clear_all", clear_all)
        setattr(wrapper, "clear_key", clear_key)

        return wrapper

    return decorator
