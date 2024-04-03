import asyncio
from itertools import count

robot_names = ['Электра', 'Механикс', 'Оптимус', 'Симулакр', 'Футуриус']
lock = asyncio.Lock()
counter = count(1)


async def coro(name: str, ind: int) -> None:
    async with lock:
        print(f'Робот {name}({ind}) передвигается к месту A')
        await asyncio.sleep(0)
        print(f'Робот {name}({ind}) достиг места A. Место A посещено {next(counter)} раз')


async def main() -> None:
    await asyncio.gather(
        *(coro(name, index) for index, name in enumerate(robot_names))
    )


if __name__ == '__main__':
    asyncio.run(main())
