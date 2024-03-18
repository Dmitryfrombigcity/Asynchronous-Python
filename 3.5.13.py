import asyncio
from time import perf_counter

start = perf_counter()


async def print_with_delay(number: int) -> None:
    await asyncio.sleep(1)
    print(f'Coroutine {number} is done')


async def main() -> None:
    tasks = [asyncio.create_task(print_with_delay(x)) for x in range(10)]
    for task in tasks:
        await task
    print(f'Elapsed time = {perf_counter() - start:_.2f}')


if __name__ == '__main__':
    asyncio.run(main())
