import asyncio


async def generate(number: int) -> None:
    print(f'Корутина generate с аргументом {number}')


async def main() -> None:
    coros = (generate(number) for number in range(10))
    await asyncio.gather(*coros)


if __name__ == '__main__':
    asyncio.run(main())
