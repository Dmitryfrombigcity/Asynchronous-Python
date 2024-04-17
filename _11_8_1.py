import asyncio
from asyncio import TaskGroup

from aiohttp import TCPConnector, ClientSession

# https://github.com/Dmitryfrombigcity/Asynchronous-Python/blob/master/_10_9_1.py
from _10_9_1 import send_result


async def coro(
        session: ClientSession,
        address: str
) -> int:
    async with session.get(address) as response:
        return response.status


async def main() -> int:
    connector = TCPConnector(limit=20)
    async with ClientSession(connector=connector) as session:
        async with TaskGroup() as group:
            tasks = [
                group.create_task(
                    coro(session, f'https://asyncio.ru/zadachi/5/{i}.html')
                ) for i in range(1, 1001)
            ]

    return sum(map(lambda x: x.result(), tasks))


if __name__ == '__main__':
    stepic = 'https://stepik.org/lesson/1075354/step/1?unit=1085452'
    send_result(asyncio.run(main()), stepic)
