import asyncio


async def coro(number: int) -> None:
    print(f'Coroutine {number} is done')


async def main() -> None:
    coros = (coro(number) for number in range(1, 4))
    await asyncio.gather(*coros)


if __name__ == '__main__':
    asyncio.run(main())
