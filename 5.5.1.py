import asyncio
import time


def print_log() -> None:
    print(f'{"":->50}',
          f'For the next loop iteration:',
          *asyncio.get_running_loop()._scheduled,
          '====>>>'
          '',
          sep='\n')


async def long_running_task(number: int) -> None:
    print(f'Task {number} started')
    await asyncio.sleep(number)
    print(f'Task {number} finished {time.monotonic() = }')
    print_log()


async def main():
    coros = (asyncio.wait_for(long_running_task(number), timeout=5) for number in range(5))

    try:
        await asyncio.gather(*coros)
    except asyncio.TimeoutError:
        print(f'Timeout, aborting {time.monotonic() = }')


if __name__ == '__main__':
    asyncio.run(main())
