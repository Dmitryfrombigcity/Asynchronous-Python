import asyncio


async def async_operation() -> None:
    print("Начало асинхронной операции.")

    try:
        await asyncio.sleep(2)
        print("Асинхронная операция успешно завершилась.")
    except asyncio.CancelledError:
        print("Асинхронная операция была отменена в процессе выполнения.")
        raise


async def main() -> None:
    print("Главная корутина запущена.")
    future = asyncio.ensure_future(async_operation())
    await asyncio.sleep(0.1)
    print("Попытка отмены Future.")
    future.cancel()

    try:
        await future
        print("Результат Future:", future.result())
    except asyncio.CancelledError:
        print("Обработка исключения: Future был отменен.")

    if future.cancelled():
        print("Проверка: Future был отменен.")
    else:
        print("Проверка: Future не был отменен.")

    print("Главная корутина завершена.")


if __name__ == '__main__':
    asyncio.run(main())
