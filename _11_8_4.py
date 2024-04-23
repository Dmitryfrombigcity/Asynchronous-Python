import asyncio

from aiohttp import TCPConnector, ClientSession
from bs4 import BeautifulSoup

# https://github.com/Dmitryfrombigcity/Asynchronous-Python/blob/master/_10_9_1.py
from _10_9_1 import send_result


async def coro(
        session: ClientSession,
        address: str,
        group: asyncio.TaskGroup,
        queue: asyncio.Queue
) -> None:
    while True:
        async with session.get(address) as response:
            if response.status != 200:
                continue

            soup = BeautifulSoup(await response.text(), 'lxml')
            if soup.find('p', id='number') is None:
                tasks = [
                    group.create_task(
                        coro(session,
                             f'{address.rsplit("/", maxsplit=1)[0]}/{page.get("href")}',
                             group,
                             queue
                             )
                    ) for page in soup.find_all('a')
                ]
                break
            else:
                await queue.put(int(soup.find('p', id='number').text))
                break


async def collect_result(queue: asyncio.Queue) -> int:
    result = 0
    while True:
        if (tmp := await queue.get()) is None:
            return result
        result += tmp


async def main(url: str) -> int:
    connector = TCPConnector(limit=0)
    queue = asyncio.Queue()
    task = asyncio.create_task(collect_result(queue))
    async with ClientSession(connector=connector) as session:
        async with asyncio.TaskGroup() as group:
            await coro(session, url, group, queue)
        await queue.put(None)
        await task
        return task.result()


if __name__ == '__main__':
    stepic = 'https://stepik.org/lesson/1075354/step/4?unit=1085452'
    url = 'https://asyncio.ru/zadachi/3/index.html'
    send_result(asyncio.run(main(url)), stepic)
