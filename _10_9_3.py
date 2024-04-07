import asyncio
import io
import zipfile
from pathlib import Path
from time import perf_counter
from typing import Any

import aiofiles
import requests

# https://github.com/Dmitryfrombigcity/Asynchronous-Python/blob/master/_10_9_1.py
from _10_9_1 import send_result


async def coro(file: Path) -> int:
    async with aiofiles.open(file) as f:
        string = await f.readline()

        # если бы csv файлы были нормальными
        # delimiter = csv.Sniffer().sniff(string.strip()).delimiter
        # return int(string.split(delimiter)[0].strip())

        return int(string.strip())


async def main() -> int:
    results: list[asyncio.Task[Any]] = []
    async with asyncio.TaskGroup() as gr:
        for file in Path('10_9_3').rglob("*.csv"):
            results.append(gr.create_task(coro(file)))
    return sum(map(lambda x: x.result(), results))


if __name__ == '__main__':
    start = perf_counter()
    stepic = 'https://stepik.org/lesson/1029069/step/3?unit=1037339'
    url = 'https://parsinger.ru/asyncio_course/5000csv.zip'
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zf:
        zf.extractall(path='10_9_3')

    result = asyncio.run(main())

    print(perf_counter() - start)
    send_result(result, stepic)
