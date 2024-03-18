# смотри комментарии на сайте
import asyncio


def print_log() -> None:
    print(f'{"":#>50}',
          f'{asyncio.get_running_loop()._ready = }',
          f'{"":->50}',
          f'{asyncio.get_running_loop()._scheduled = }',
          f'{"":->50}',
          *asyncio.all_tasks(),
          f'{"":#>50}',
          '',
          sep='\n')


async def coro(n: int) -> None:
    print(f"Задача {n} запустилась, будет работать {n} сек.")
    t = asyncio.current_task()
    t.cancel()
    print_log()
    await asyncio.sleep(n)

    print(f"Задача {n} завершилась после {n} сек.")
    print_log()


async def coro_extra(n: int) -> None:
    print(f"Задача {n} запустилась, будет работать {n} сек.")
    print("Создание Task-5")
    task_5 = asyncio.create_task(coro(5), name='Task-5')
    print_log()
    await asyncio.sleep(n)
    print(f"Задача {n} завершилась после {n} сек.")
    print_log()


async def main():
    print("Создание Task-2, Task-3")
    task_2 = asyncio.create_task(coro(2), name='Task-2')
    task_3 = asyncio.create_task(coro(3), name='Task-3')
    print_log()
    await asyncio.gather(task_2, task_3, return_exceptions=True)
    print("Создание Task-4, Task-6")
    task_4 = asyncio.create_task(coro_extra(4), name='Task-4')
    task_6 = asyncio.create_task(coro(6), name='Task-6')
    print_log()


asyncio.run(main())
print('Конец')
