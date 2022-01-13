# Tempo

[![Coverage Status](./reports/coverage/coverage-badge.svg?dummy=8484744)](./reports/coverage/cov_html/index.html)  [![Tests](./reports/coverage/tests-badge.svg?dummy=8484744)](./reports/coverage/cov_html/index.html) 

*Asynchronous wrapper for HTTP requests.*

## Installation

```bash
pip install tempo-async
```

## Usage

```python
import tempo

url = 'https://via.placeholder.com'
num_reqs = 100

requests = [ # map in any request parameters: url, query params, HTTP method, etc.
  tempo.RequestConfig(url=url) for _ in range(num_reqs)
]

if __name__ == '__main__':
  tempo.run(requests, rate=10) # fetch 100 cat pictures, 10 a second
```

Take it a step further by collecting the responses,

```python
import tempo

url = 'https://via.placeholder.com'
num_reqs = 100

### cat picture bucket
catpics = []
###

requests = [ # map in any request parameters: url, query params, HTTP method, etc.
  tempo.RequestConfig(url=url) for _ in range(num_reqs)
]

if __name__ == '__main__':
  tempo.run(requests, collector=catpics, rate=10) # indicated `catpics` should store response
  print(f'Pictures stored in list: {len(catpics)}')
```

… and adding any number of processing functions to handle responses.

```python
import tempo

url = 'https://via.placeholder.com'
num_reqs = 100
catpics = []

requests = [ # map in any request parameters: url, query params, HTTP method, etc.
  tempo.RequestConfig(url=url) for _ in range(num_reqs)
]

### processors
def say_hi(res) -> None:
  # returns None so does not affect final processed response sent to collectors
  print('Hello cat!')

def get_body(res) -> str:
  # since it returns a value, this processor changes the final output of `tempo.run`
  body = res.text
  return body
###

if __name__ == '__main__':
  # process the requests in order of listed processors
  tempo.run(requests, collector=catpics, rate=10, processors=[say_hi, get_body])
  # processors' return values affect output sent to collectors
  print(f'Type of stored result: {type(catpics[0])}') # str, not Response object
```



## Contributing

Submit a pull request! Contributions are welcome!

Please write test coverage for your changes and run `tox` to test for backwards compatibility among the supported Python versions.

## TODOS

Open an issue, create a branch, and submit a PR. (Tests for everything!)

- Handle collection of results as a return value of the `run` function.
- Decorator for basic async request function accepting iterator of request arguments.
- Accept plain Python dictionaries and JSON in addition to RequestConfig objects for requests mapping.
- Logging.
- Exception handling.
- GitHub Actions.
- Retries with various back-off algorithms and HTTP response header search for 429 causes.
- Generator option for `run` function.
- Allow `collector` argument to be an iterable, a function passed a response / processed response object, or a file out. Maybe even stdout.
- Like processors, allow multiple collectors (eg. file, queue).
- Local database for keeping track of requests and their status, for retry and interrupts.
- Asynchronous processor support.
- Handle streaming responses.
- CLI
- Documentation page. Also, good docstrings.
- Test coverage tracking.
- …
