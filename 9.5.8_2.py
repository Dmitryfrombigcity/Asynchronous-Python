import asyncio
from dataclasses import dataclass


@dataclass
class ControlSystem:
    semaphore: asyncio.Semaphore
    counter: int = 0

    async def user_request(
            self,
            name: str
    ) -> None:
        async with self.semaphore:
            print(f'Пользователь {name} делает запрос')
            self.counter += 1
            await asyncio.sleep(0)
            print(f'Запрос от пользователя {name} завершен')
        print(f'Всего запросов: {self.counter}')


async def main() -> None:
    users = [
        "sasha", "petya", "masha", "katya", "dima", "olya", "igor", "sveta", "nikita", "lena",
        "vova", "yana", "kolya", "anya", "roma", "nastya", "artem", "vera", "misha", "liza"
    ]
    process = ControlSystem(asyncio.Semaphore(3))
    await asyncio.gather(*(process.user_request(user) for user in users))


if __name__ == '__main__':
    asyncio.run(main())
