import asyncio
import io
import zipfile
from pathlib import Path
from time import perf_counter, sleep
from typing import Any

import aiofiles
import requests
from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def send_result(
        result: int,
        stepic: str
) -> None:
    env = Env()
    env.read_env(recurse=False)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 15)
        driver.get(stepic)
        driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
        driver.refresh()
        wait.until(
            ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//input'))
        ).send_keys(str(result))
        wait.until(
            ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
        ).click()
        sleep(1)


async def coro(file: Path) -> int:
    async with aiofiles.open(file) as f:
        num = await f.readline()
        return tmp \
            if not (tmp := int(num.strip())) % 2 \
            else 0


async def main() -> int:
    results: list[asyncio.Task[Any]] = []
    async with asyncio.TaskGroup() as gr:
        for file in Path('10_9_1').rglob("*.txt"):
            results.append(gr.create_task(coro(file)))
    return sum(map(lambda x: x.result(), results))


if __name__ == '__main__':
    start = perf_counter()
    stepic = 'https://stepik.org/lesson/1029069/step/1?thread=solutions&unit=1037339'
    url = 'https://parsinger.ru/asyncio_course/files.zip'
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zf:
        zf.extractall(path='10_9_1')

    result = asyncio.run(main())

    print(perf_counter() - start)
    send_result(result, stepic)
