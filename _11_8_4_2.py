import asyncio

from aiohttp import TCPConnector, ClientSession
from bs4 import BeautifulSoup

# https://github.com/Dmitryfrombigcity/Asynchronous-Python/blob/master/_10_9_1.py
from _10_9_1 import send_result


async def coro(
        session: ClientSession,
        address: str
) -> int:
    async with asyncio.TaskGroup() as group:
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
                                 )
                        ) for page in soup.find_all('a')
                    ]
                    break
                else:
                    return int(soup.find('p', id='number').text)

    return sum(map(lambda task: task.result(), tasks))


async def main(url: str) -> int:
    connector = TCPConnector(limit=0)
    async with ClientSession(connector=connector) as session:
        return await coro(session, url)


if __name__ == '__main__':
    stepic = 'https://stepik.org/lesson/1075354/step/4?unit=1085452'
    url = 'https://asyncio.ru/zadachi/3/index.html'
    send_result(asyncio.run(main(url)), stepic)
