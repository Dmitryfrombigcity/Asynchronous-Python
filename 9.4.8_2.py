import asyncio


async def control(condition: asyncio.Condition) -> None:
    async with condition:
        condition.notify()


async def coro(user: str, condition: asyncio.Condition) -> None:
    async with condition:
        print(f'Пользователь {user} ожидает доступа к базе данных')
        await condition.wait()
        print(f'''Пользователь {user} подключился к БД
Пользователь {user} отключается от БД''')
        condition.notify()


async def main():
    users = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eva', 'Frank', 'George', 'Helen', 'Ivan', 'Julia']
    condition = asyncio.Condition()
    await asyncio.gather(*(coro(user, condition) for user in users), control(condition))


if __name__ == '__main__':
    asyncio.run(main())
