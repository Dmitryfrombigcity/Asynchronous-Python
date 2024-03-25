import asyncio


async def failing_coroutine():
    await asyncio.sleep(1)
    raise ValueError("Возникла ошибка в корутине failing_coroutine()")


async def successful_coroutine():
    await asyncio.sleep(1)
    print("Успешное выполнение")


async def main():
    tasks = [asyncio.create_task(failing_coroutine()),
             asyncio.create_task(successful_coroutine())]

    fut = asyncio.gather(*tasks)
    fut.cancel()
    try:
        await fut
    except asyncio.CancelledError:
        pass


asyncio.run(main())
