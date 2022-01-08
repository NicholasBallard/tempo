import httpx
import asyncio
import time

async def get_async(url):
    async with httpx.AsyncClient() as client:
        return await client.get(url)

urls = ['http://webcode.me', 'https://httpbin.org/get', 
    'https://google.com', 'https://stackoverflow.com', 
    'https://github.com']

async def launch():
    resps = await asyncio.gather(*map(get_async, urls))
    data = [resp.status_code for resp in resps]
    
    for status_code in data:
        print(status_code)

start_time = time.monotonic()
asyncio.run(launch())
print(f'Elapsed: {time.monotonic() - start_time}')