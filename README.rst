# Tempo

*Asynchronous wrapper for HTTP requests.*

## Installation

```bash
pip install tempo-async
```

## Usage

```python
from tempo import run, tempo

@tempo(rps=10, retry=3)
def fetch_cat_pics(urls: list[str], **params):
  import time
  for url in urls:
  	time.sleep(1)
    try:
	  	res = requests.request('GET', url, **params)
  		res.raise_for_status()
      yield res
     except:
      continue

      
if __name__ == '__main__':
  cat_pics = ['https://via.placeholder.com'] * 10
  run(fetch_cat_pics(cat_pics))
```



## Contributing

Submit a pull request! Contributions are welcome!

Please write test coverage for your changes and run `tox` to test for backwards compatibility among the supported Python versions.

