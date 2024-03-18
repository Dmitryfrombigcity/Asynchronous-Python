import asyncio
from time import perf_counter

start = perf_counter()

max_counts = {
    "Counter 1": 13,
    "Counter 2": 7
}
counts = {}


async def counter(name: str, delay: float) -> None:
    while counts.setdefault(name, 0) < max_counts[name]:
        counts[name] += 1
        await asyncio.sleep(delay)
        print(f'{name}: {counts[name]}')


async def main() -> None:
    task_1 = asyncio.create_task(counter(name='Counter 1', delay=0.1))
    task_2 = asyncio.create_task(counter(name='Counter 2', delay=0.1))
    await asyncio.gather(task_1, task_2)
    print(f'Elapsed time = {perf_counter() - start:_.2f}')


if __name__ == '__main__':
    asyncio.run(main())
