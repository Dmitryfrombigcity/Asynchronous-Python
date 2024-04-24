import asyncio

from aiohttp import TCPConnector, ClientSession
from bs4 import BeautifulSoup

# https://github.com/Dmitryfrombigcity/Asynchronous-Python/blob/master/_10_9_1.py
from _10_9_1 import send_result


async def coro(
        session: ClientSession,
        address: str
) -> int:
    while True:
        async with session.head(address) as response:
            if response.status != 200:
                continue
            return int(response.headers['Content-Length'])


async def main(url: str) -> int:
    connector = TCPConnector(limit=100)
    async with ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'lxml')
            else:
                raise Exception("Something wrong with the website")
            async with asyncio.TaskGroup() as group:
                tasks = [
                    group.create_task(
                        coro(
                            session,
                            f'https://asyncio.ru/zadachi/4/{item.get("src")}'
                        )
                    )
                    for item in soup.find_all('img')

                ]

            return sum(map(lambda task: task.result(), tasks))


if __name__ == '__main__':
    stepic = 'https://stepik.org/lesson/1075354/step/5?unit=1085452'
    url = 'https://asyncio.ru/zadachi/4/index.html'
    asyncio.run(main(url))
    send_result(asyncio.run(main(url)), stepic)
