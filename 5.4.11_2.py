import asyncio


async def countdown(
        name: str,
        seconds: int
) -> None:
    while seconds:
        print(f'{name}: Осталось {seconds} сек. {asyncio.current_task().get_name()}')
        seconds -= 1
        await asyncio.sleep(delay=1)
    print(f'{name}: Задание выполнено! Что дальше?')


async def main():
    treasure_hunt = asyncio.create_task(
        countdown(name='Квест на поиск сокровищ', seconds=10),
        name='Найди скрытые сокровища!'
    )
    dragon_escape = asyncio.create_task(
        countdown(name='Побег от дракона', seconds=5),
        name='Беги быстрее, дракон на хвосте!'
    )
    await asyncio.gather(treasure_hunt, dragon_escape)


if __name__ == "__main__":
    asyncio.run(main())
