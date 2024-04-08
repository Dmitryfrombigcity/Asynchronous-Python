import asyncio


async def control(condition: asyncio.Condition) -> None:
    try:
        while True:
            async with condition:
                condition.notify()
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        pass


async def coro(user: str, condition: asyncio.Condition) -> None:
    async with condition:
        print(f'Пользователь {user} ожидает доступа к базе данных')
        await condition.wait()
        print(f'''Пользователь {user} подключился к БД
Пользователь {user} отключается от БД''')


async def main():
    users = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eva', 'Frank', 'George', 'Helen', 'Ivan', 'Julia']
    condition = asyncio.Condition()
    task = asyncio.create_task(control(condition))
    await asyncio.gather(*(coro(user, condition) for user in users))
    task.cancel()
    await task


if __name__ == '__main__':
    asyncio.run(main())
