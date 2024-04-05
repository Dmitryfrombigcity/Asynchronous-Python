import asyncio
import io
import zipfile
from asyncio import Queue
from pathlib import Path
from time import perf_counter

import aiofiles
import requests


async def get_result(queue: Queue):
    result = 0
    while True:
        res: str = await queue.get()
        if res == 'END':
            break
        elif not (tmp := int(res.strip())) % 2:
            result += tmp
        queue.task_done()
    return result


async def coro(queue, file):
    async with aiofiles.open(file) as f:
        num = await f.readline()
        await queue.put(num)


async def main():
    queue = asyncio.Queue()
    task = asyncio.create_task(get_result(queue))
    async with asyncio.TaskGroup() as gr:
        for file in Path('10_9_1').rglob("*.txt"):
            gr.create_task(coro(queue, file))
    await queue.join()
    await queue.put('END')
    print(await task)


if __name__ == '__main__':
    start = perf_counter()
    url = 'https://parsinger.ru/asyncio_course/files.zip'
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zf:
        zf.extractall(path='10_9_1')
    asyncio.run(main())
    print(perf_counter() - start)
