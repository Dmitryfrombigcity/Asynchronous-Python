import asyncio
import csv
import json
from pathlib import Path
from time import perf_counter, sleep
from typing import Type

import aiocsv
import aiofiles
import requests
from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def load_file(url: str) -> Type[csv.Dialect]:
    """
    Загружаем файл в каталог Path.cwd()/10_9_5
    и определяем его диалект.
    Если каталог не существует, то создаём его.
    :param url: Адрес файла.
    :return: Диалект файла.
    """
    if not (Path.cwd() / '10_9_5').exists():
        (Path.cwd() / '10_9_5').mkdir()
    response = requests.get(url)
    response.encoding = 'utf-8-sig'
    with open(path_csv, mode='w+') as file:
        file.write(response.text)
        file.seek(0)
        test = file.read(4096)
        return csv.Sniffer().sniff(test)


async def convert(queue: asyncio.Queue) -> None:
    """
    Берём данные из очереди и записываем их в json-файл.
    Создаётся файл Path.cwd()/10_9_5/file.json,
    если файл уже существует, он пересоздаётся.
    Время работы 1550 сек.
    :param queue: Очередь из которой поступают данные.
    """
    if path_json.exists():
        path_json.unlink()
    path_json.touch()
    while True:
        with open(path_json, 'r+') as file:
            if not path_json.stat().st_size:
                items = [await queue.get()]
            else:
                items = [*json.load(file), await queue.get()]
            file.seek(0)
            json.dump(items, file, ensure_ascii=False, indent=4)
            queue.task_done()


async def convert_mod(queue: asyncio.Queue) -> None:
    """
    Берём данные из очереди и записываем их в json-файл.
    Создаётся файл Path.cwd()/10_9_5/file.json,
    если файл уже существует, он пересоздаётся.
    Время работы 190 сек.
    :param queue: Очередь из которой поступают данные.
    """
    if path_json.exists():
        path_json.unlink()
    path_json.touch()
    while True:
        with open(path_json, 'r+') as file:
            items = json.dumps(
                [await queue.get()],
                ensure_ascii=False,
                indent=4
            )
            if path_json.stat().st_size:
                items = f'{file.read()[:-2]},{items[1:]}'
                file.seek(0)
            file.write(items)
            queue.task_done()


def send_result(
        stepic: str,
        validation: str
) -> None:
    """
    Валидируем json-файл и вводим ключ на stepik'е.
    :param stepic: URL страницы stepik'а.
    :param validation: URL валидатора.
    """
    env = Env()
    env.read_env(recurse=False)
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')

    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 15)

        driver.get(validation)
        wait.until(
            ec.visibility_of_element_located(('tag name', 'input'))
        ).send_keys(path_json.as_posix())
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


async def main(dialect: Type[csv.Dialect]) -> None:
    """
    Асинхронно читаем csv-файл и записываем результаты в очередь.
    Запускаем задачу для конвертации csv-файла в json-файл.
    Когда все данные считаны, закрываем задачу.
    :param dialect: Диалект csv-файла.
    """
    queue = asyncio.Queue()
    task = asyncio.create_task(convert_mod(queue))
    async with aiofiles.open(path_csv) as file:
        async_reader = aiocsv.AsyncDictReader(file, dialect=dialect)
        async for item in async_reader:
            await queue.put(item)
            print(queue.qsize())  # показывает как живёт очередь
        await queue.join()
        task.cancel()


if __name__ == '__main__':
    csv_url = 'https://parsinger.ru/asyncio_course/1/adress_1000000.csv'
    validator_url = 'https://parsinger.ru/asyncio_course/1/test/Index.html'
    stepic_url = 'https://stepik.org/lesson/1029069/step/5?unit=1037339'
    path_csv = Path(Path.cwd(), '10_9_5', 'file.csv')
    path_json = Path(Path.cwd(), '10_9_5', 'file.json')
    dialect = load_file(csv_url)
    start = perf_counter()
    asyncio.run(main(dialect))
    print(perf_counter() - start)
    send_result(stepic_url, validator_url)
