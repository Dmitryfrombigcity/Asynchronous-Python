import asyncio

requests = 0


async def coro(
        sem: asyncio.Semaphore,
        user: str
) -> None:
    global requests
    async with sem:
        print(f'Пользователь {user} делает запрос')
        requests += 1
        await asyncio.sleep(0)
        print(f'Запрос от пользователя {user} завершен')
    print(f'Всего запросов: {requests}')


async def main() -> None:
    users = [
        "sasha", "petya", "masha", "katya", "dima", "olya", "igor", "sveta", "nikita", "lena",
        "vova", "yana", "kolya", "anya", "roma", "nastya", "artem", "vera", "misha", "liza"
    ]
    sem = asyncio.Semaphore(3)
    await asyncio.gather(*(coro(sem, user) for user in users))


if __name__ == '__main__':
    asyncio.run(main())
