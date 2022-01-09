import pytest
import nest_asyncio
nest_asyncio.apply()

from tempo.ratelimiter import (
    RateLimiter,
)
from tempo.run import RequestConfig


@pytest.mark.asyncio
async def test_ratelimiter():
    RateLimiter(3, 3)
    assert True
