from pydantic import (
    AnyHttpUrl,
    BaseModel,
    validator,
)
import asyncio
from functools import partial, wraps
from typing import (
    Awaitable,
    Callable,
    Coroutine,
    Iterable,
)

import httpx
import nest_asyncio
nest_asyncio.apply()

from .ratelimiter import RateLimiter


class RequestConfig(BaseModel):
    method: str = 'GET'
    url: AnyHttpUrl
    params: dict = {}
    data: dict = {}
    headers: dict = {}

    @validator('method')
    def method_validator(cls, v):
        if v not in ['GET', 'POST', 'PUT', 'DELETE']:
            raise ValueError(f'{v} is not a valid method')
        return v


def asyncio_run(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        asyncio.run(f(*args, **kwargs))
    return wrapper


@asyncio_run
async def run(
    requests: list[RequestConfig],
    collector: list = None,
    rate: int = 10,
    con_limit: int = 10,
    processors: list[Callable] = None
) -> Iterable[Coroutine]:
    """Run the requests"""
    limiter: RateLimiter = RateLimiter(rate, con_limit)

    def throttle(f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            async with limiter.throttle():
                return await f(*args, **kwargs)
        return wrapper

    @throttle
    async def _req(client, config: RequestConfig):
        return await client.request(**config.dict())

    # TODO handle collection
    def handle_collection(res):
        ...
    
    # TODO yield res
    
    # TODO return grouped results option

    def process(res):
        if not processors:
            return res
        for process in processors:
            if (processed := process(res)):
                res = processed
        return res

    async with limiter:
        async with httpx.AsyncClient() as client:
            coros: Iterable[Awaitable] = map(partial(_req, client), requests)
            for coroutine in asyncio.as_completed(coros):
                res = await coroutine
                processed = process(res)
                if collector is not None:
                    collector.append(processed)
            return coros
