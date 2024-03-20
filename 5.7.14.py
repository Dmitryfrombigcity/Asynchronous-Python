import asyncio

dishes = {
    'Куриный суп': 118,
    'Бефстроганов': 13,
    'Рататуй': 49,
    'Лазанья': 108,
    'Паэлья': 51,
    'Утка по-пекински': 41,
}


async def cook_dish(name: str, duration: float) -> None:
    print(f'Приготовление {name} начато.')
    await asyncio.sleep(duration / 10)
    print(f'Приготовление {name} завершено. за {duration / 10}')


async def main() -> None:
    tasks = [
        asyncio.create_task(cook_dish(name, duration), name=name
                            ) for name, duration in dishes.items()
    ]
    done, pending = await asyncio.wait(tasks, timeout=10)
    for task in pending:
        print(f'{task.get_name()} не успел(а,о) приготовиться и будет отменено.')
    print(f'\n'
          f'Приготовлено блюд: {len(done)}.'
          f' Не успели приготовиться: {len(pending)}.')


if __name__ == '__main__':
    asyncio.run(main())
