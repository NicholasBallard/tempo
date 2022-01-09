import time

import pytest

from tempo.run import (
    RequestConfig,
    run
)


@pytest.fixture
def url():
    return 'https://jsonplaceholder.typicode.com/todos/'


def process_1(res):
    body = res.json()
    print(body.get('id'))


def process_2(res):
    # insert time into response body
    body = res.json()
    body.update({'time': time.time()})


# @pytest.mark.asyncio
def test_run_rate_limiter(url):
    prepped_reqs = [RequestConfig(url=f'{url}{i}') for i in range(1, 25)]
    collector = []
    # run requests
    t0 = time.time()
    run(
        requests=prepped_reqs,
        collector=collector,
        rate=10,
        con_limit=10,
        processors=[process_1, process_2]
    )
    time_ = time.time() - t0
    assert time_ < 1.5
