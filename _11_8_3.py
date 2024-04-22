import asyncio
from asyncio import TaskGroup

import requests
from aiohttp import TCPConnector, ClientSession
from bs4 import BeautifulSoup

# https://github.com/Dmitryfrombigcity/Asynchronous-Python/blob/master/_10_9_1.py
from _10_9_1 import send_result


async def coro(
        session: ClientSession,
        address: str
) -> int:
    while True:
        async with session.get(address) as response:
            if response.status != 200:
                continue
            soup = BeautifulSoup(await response.text(), 'lxml')
            return int(soup.find('p', id='number').text)


async def main(pages: list[str]) -> int:
    connector = TCPConnector(limit=75)
    async with ClientSession(connector=connector) as session:
        async with TaskGroup() as group:
            tasks = [
                group.create_task(
                    coro(session,
                         f'https://asyncio.ru/zadachi/2/html/{page}.html')
                ) for page in pages
            ]

    return sum(map(lambda task: task.result(), tasks))


if __name__ == '__main__':
    stepic = 'https://stepik.org/lesson/1075354/step/3?unit=1085452'
    url = 'https://asyncio.ru/zadachi/2/problem_pages.txt'
    pages = requests.get(url)
    soup = BeautifulSoup(pages.text, 'lxml')
    pages_lst = soup.get_text().split()
    send_result(asyncio.run(main(pages_lst)), stepic)
