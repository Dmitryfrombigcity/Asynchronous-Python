import asyncio


async def set_future_result(value: str, delay: float) -> str:
    print(f"Задача начата. Установка результата '{value}' через {delay} секунд.")
    await asyncio.sleep(delay)
    print("Результат установлен.")
    return value


async def create_and_use_future() -> str:
    future = asyncio.ensure_future(set_future_result('Успех', 2))

    if future.done():
        print("Состояние Future до выполнения: Завершено")
    else:
        print("Состояние Future до выполнения: Ожидание")
    print("Задача запущена, ожидаем завершения...")
    result = await future

    if future.done():
        print("Состояние Future после выполнения: Завершено")
    else:
        print("Состояние Future после выполнения: Ожидание")

    return result


async def main() -> None:
    result = await create_and_use_future()
    print("Результат из Future:", result)


if __name__ == '__main__':
    asyncio.run(main())
