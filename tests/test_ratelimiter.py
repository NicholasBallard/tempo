import pytest

from tempo.ratelimiter import RateLimiter


@pytest.mark.asyncio
async def test_ratelimiter():
    RateLimiter(3,3)
    assert True