import asyncio
import io
import json
import zipfile
from datetime import datetime
from pathlib import Path
from time import perf_counter, sleep
from typing import Any

import aiocsv
import aiofiles
import requests
from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


async def coro(
        path_to_file: Path,
        queue: asyncio.Queue[dict[str, Any] | None],
        sem: asyncio.Semaphore
) -> None:
    async with sem:
        async with aiofiles.open(path_to_file) as file:
            contents = json.loads(await file.read())
            for item in contents:
                if item.get('HTTP-статус') == 200:
                    await queue.put(item)


async def collect_result(
        queue: asyncio.Queue[dict[str, Any] | None]
) -> None:
    results: list[dict[str, Any]] = []
    while True:
        if (result := await queue.get()) is None:
            break
        results.append(result)
    results.sort(
        key=lambda item: item['Время и дата']
    )
    for result in results:
        result['Время и дата'] = (
            datetime.strptime(result['Время и дата'], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M:%S')
        )

    async with aiofiles.open(
            path_csv,
            mode='w',
            encoding='utf-8-sig',
            newline=''
    ) as file:
        writer = aiocsv.AsyncDictWriter(
            file,
            fieldnames=list(results[0].keys()),
            lineterminator="\n",
            delimiter=";"
        )
        await writer.writeheader()
        await writer.writerows(results)


async def main(sub_dir: str) -> None:
    queue: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue()
    sem: asyncio.Semaphore = asyncio.Semaphore(1000)
    task = asyncio.create_task(collect_result(queue))
    async with asyncio.TaskGroup() as group:
        for file in Path(sub_dir).rglob("*.json"):
            group.create_task(coro(file, queue, sem))
    await queue.put(None)
    await task


def send_result(
        stepic: str,
        validation: str
) -> None:
    env = Env()
    env.read_env(recurse=False)
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')

    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 30)

        driver.get(validation)
        wait.until(
            ec.visibility_of_element_located(('tag name', 'input'))
        ).send_keys(path_csv.as_posix())
        wait.until(
            ec.element_to_be_clickable(('tag name', 'button'))
        ).click()

        code = wait.until(
            ec.presence_of_element_located(('xpath', '//*[@id="resultsTable"]/p'))
        ).text

        driver.get(stepic)
        driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
        driver.refresh()
        wait.until(
            ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//textarea'))
        ).send_keys(code.split(':')[-1].strip())
        wait.until(
            ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
        ).click()
        sleep(1)


if __name__ == '__main__':
    validator_url = 'https://parsinger.ru/asyncio_course/5/test/Index.html'
    stepic_url = 'https://stepik.org/lesson/1029069/step/8?unit=1037339'
    url = 'https://parsinger.ru/asyncio_course/logs.zip'
    sub_dir = '10_9_8'
    path_csv = Path(Path.cwd(), '10_9_8', 'file.csv')
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zf:
        zf.extractall(path=sub_dir)

    start = perf_counter()
    asyncio.run(main(sub_dir))

    print(perf_counter() - start)
    send_result(stepic_url, validator_url)
