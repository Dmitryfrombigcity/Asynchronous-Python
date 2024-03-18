import asyncio
from time import perf_counter

start = perf_counter()


async def first_function(x: int) -> int:
    print(f"Выполняется первая функция с аргументом {x}")
    await asyncio.sleep(1)
    result = x + 1
    print(f"Первая функция завершилась с результатом {result}")
    return result


async def second_function(x: int) -> int:
    print(f"Выполняется вторая функция с аргументом {x}")
    await asyncio.sleep(1)
    result = x * 2
    print(f"Вторая функция завершилась с результатом {result}")
    return result


async def third_function(x: int) -> int:
    print(f"Выполняется третья функция с аргументом {x}")
    await asyncio.sleep(1)
    result = x + 3
    print(f"Третья функция завершилась с результатом {result}")
    return result


async def fourth_function(x: int) -> int:
    print(f"Выполняется четвертая функция с аргументом {x}")
    await asyncio.sleep(1)
    result = x ** 2
    print(f"Четвертая функция завершилась с результатом {result}")
    return result


async def main() -> None:
    print("Начало цепочки асинхронных вызовов")
    first = await asyncio.ensure_future(first_function(1))
    second = await asyncio.ensure_future(second_function(first))
    third = await asyncio.ensure_future(third_function(second))
    final_result = await asyncio.ensure_future(fourth_function(third))
    print(f"Конечный результат цепочки вызовов: {final_result}")

    # print(f'Elapsed time = {perf_counter() - start:_.2f}')


if __name__ == '__main__':
    asyncio.run(main())
