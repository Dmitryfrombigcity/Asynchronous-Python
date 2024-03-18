import asyncio
from time import perf_counter

start = perf_counter()

max_counts = {
    "Counter 1": 10,
    "Counter 2": 5,
    "Counter 3": 15
}
delays = {
    "Counter 1": 1,
    "Counter 2": 2,
    "Counter 3": 0.5
}
counts = {}


async def counter(name: str) -> None:
    while counts.setdefault(name, 0) < max_counts[name]:
        counts[name] += 1
        await asyncio.sleep(delays.get(name))
        print(f'{name}: {counts[name]}')


async def main() -> None:
    await asyncio.gather(*(counter(name) for name in max_counts.keys()))
    print(f'Elapsed time = {perf_counter() - start:_.2f}')



if __name__ == '__main__':
    asyncio.run(main())
