import asyncio
from time import perf_counter


async def my_coroutine(ind: int) -> int:
    print(f'{"":#>25}'
          f' Задача {asyncio.current_task().get_name()} запустилась',
          *asyncio.all_tasks(), '', sep='\n')
    await asyncio.sleep(ind)
    print(f'{"":#>25}'
          f' Задача {asyncio.current_task().get_name()} завершилась',
          *asyncio.all_tasks(), '', sep='\n')
    return ind


async def main() -> None:
    # coros_1 = [
    #     asyncio.wait_for(
    #         my_coroutine(index), timeout=5
    #     ) for index in range(1, 3)
    # ]
    tasks = [
        asyncio.create_task(
            asyncio.wait_for(my_coroutine(index), timeout=5)
        ) for index in range(1, 3)
    ]
    # coros_2 = [
    #     asyncio.wait_for(
    #         asyncio.create_task(my_coroutine(index)), timeout=5
    #     ) for index in range(1, 3)
    # ]

    print(f'{"":#>25} Before first switch',
          *asyncio.all_tasks(), '', sep='\n')
    await asyncio.sleep(0)
    print(f'{"":#>25} After first switch',
          *asyncio.all_tasks(), '', sep='\n')

    tasks_lst = asyncio.all_tasks()
    print(f'{"":#>25} Await tasks')
    for task in tasks:
        await task
    print(f'{"":#>25} Finished tasks=',
          *tasks_lst, sep='\n')

    # Python 3.11
    #
    # tasks => tasks_lst =>
    # <Task finished name='Task-3' coro=<wait_for() done> result=2>
    # <Task finished name='Task-4' coro=<my_coroutine() done> result=1>
    # <Task finished name='Task-2' coro=<wait_for() done> result=1>
    # <Task pending name='Task-1' coro=<main() > cb=[_run_until_complete_cb()]>
    # <Task finished name='Task-5' coro=<my_coroutine() done,> result=2>
    #
    # coros_2 => tasks_list =>
    # <Task pending name='Task-1' coro=<main()> cb=[_run_until_complete_cb()>
    # <Task finished name='Task-2' coro=<my_coroutine() done> result=1>
    # <Task finished name='Task-3' coro=<my_coroutine() done> result=2>


start = perf_counter()
asyncio.run(main())
print(perf_counter() - start)
