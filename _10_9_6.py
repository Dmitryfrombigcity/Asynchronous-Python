import asyncio
import csv
import io
import json
import zipfile
from pathlib import Path
from time import perf_counter, sleep
from typing import Type, Mapping

import aiocsv
import aiofiles
import requests
from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


async def coro(
        path_to_file: Path,
        queue: asyncio.Queue[Mapping[str, str] | None],
        sem: asyncio.Semaphore
) -> None:
    async with sem:
        dialect: Type[csv.Dialect] = get_dialect(path_to_file)
        async with aiofiles.open(path_to_file, encoding='utf-8-sig') as file:
            async_reader = aiocsv.AsyncDictReader(file, dialect=dialect)
            async for item in async_reader:
                if item.get('Балл ЕГЭ') == '100':
                    await queue.put(item)

                # Показывает как именно итерируется файл
                # print(
                #     asyncio.current_task().get_coro(),
                #     asyncio.current_task().get_name(),
                #     queue.qsize()
                # )


def get_dialect(path_to_file: Path) -> Type[csv.Dialect]:
    with open(path_to_file, mode='r', encoding='utf-8-sig') as file:
        test = file.read(4096)
        return csv.Sniffer().sniff(test)


async def collect_result(
        queue: asyncio.Queue[Mapping[str, str] | None]
) -> None:
    results: list[Mapping[str, str]] = []
    while True:
        if (result := await queue.get()) is None:
            break
        results.append(result)
    results.sort(key=lambda x: x['Телефон для связи'])
    async with aiofiles.open(path_json, mode='w') as file:
        await file.write(
            json.dumps(
                results,
                ensure_ascii=False,
                indent=4
            )
        )


async def main(sub_dir: str) -> None:
    queue: asyncio.Queue[Mapping[str, str] | None] = asyncio.Queue()
    sem: asyncio.Semaphore = asyncio.Semaphore(1000)
    task = asyncio.create_task(collect_result(queue))
    async with asyncio.TaskGroup() as group:
        for file in Path(sub_dir).rglob("*.csv"):
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
        ).send_keys(path_json.as_posix())
        wait.until(
            ec.element_to_be_clickable(('tag name', 'button'))
        ).click()

        result_message = driver.find_element('id', 'resultMessage')
        wait.until(
            lambda _: result_message.text != ''
        )
        code = result_message.text

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
    validator_url = 'https://asyncio.ru/zadachi/10.9/6/Index.html'
    stepic_url = 'https://stepik.org/lesson/1029069/step/6?unit=1037339'
    url = 'https://asyncio.ru/zadachi/10.9/6/region_student.zip'
    sub_dir = '10_9_6'
    path_json = Path(Path.cwd(), '10_9_6', 'file.json')
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content), 'r', metadata_encoding='cp866') as zf:
        zf.extractall(path=sub_dir)

    start = perf_counter()
    asyncio.run(main(sub_dir))
    print(perf_counter() - start)
    send_result(stepic_url, validator_url)
