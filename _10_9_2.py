import asyncio
import io
import json
import zipfile
from pathlib import Path
from time import perf_counter, sleep

import aiofiles
import requests
from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def send_result(
        result: dict[str, str],
        stepic: str,
        validation: str
) -> None:
    env = Env()
    env.read_env(recurse=False)
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')

    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 15)

        driver.get(validation)
        wait.until(
            ec.visibility_of_element_located(('tag name', 'textarea'))
        ).send_keys(json.dumps(result, ensure_ascii=False, indent=4))
        wait.until(
            ec.element_to_be_clickable(('tag name', 'button'))
        ).click()
        code = wait.until(
            ec.presence_of_element_located(('id', 'output'))
        ).text

        driver.get(stepic)
        driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
        driver.refresh()
        wait.until(
            ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//textarea'))
        ).send_keys(code)
        wait.until(
            ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
        ).click()
        sleep(1)


async def coro(
        file: Path,
        record_dict: dict[str, float]
) -> None:
    async with aiofiles.open(file) as f:
        for record in await f.readlines():
            record = record.split('-')[-1]
            key, value = record.split(':')
            key = key.strip()
            record_dict[key] = record_dict.get(key, 0) + len(value.strip()) * 0.03


async def main() -> dict[str, str]:
    record_dict: dict[str, float] = {}
    async with asyncio.TaskGroup() as gr:
        for file in Path('10_9_2').rglob("*.txt"):
            gr.create_task(coro(file, record_dict))
    result_dict = {
        key: f'{round(value, 2)}р' for key, value in
        sorted(record_dict.items(), key=lambda x: x[-1], reverse=True)
    }
    return result_dict


if __name__ == '__main__':
    start = perf_counter()
    validation = 'https://parsinger.ru/asyncio_course/7/Index.html'
    stepic = 'https://stepik.org/lesson/1029069/step/2?unit=1037339'
    url = 'https://parsinger.ru/asyncio_course/chat_log.zip'
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zf:
        zf.extractall(path='10_9_2')

    result = asyncio.run(main())

    print(perf_counter() - start)
    send_result(result, stepic, validation)
