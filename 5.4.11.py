# For version 3.11
import asyncio
import contextvars

var = contextvars.ContextVar('var')


async def countdown(
        name: str,
        seconds: int
) -> None:
    while seconds:
        print(f'{name}: Осталось {seconds} сек. {var.get()}')
        seconds -= 1
        await asyncio.sleep(delay=1)
    print(f'{name}: Задание выполнено! Что дальше?')


async def main():
    var.set('Найди скрытые сокровища!')
    content_1 = contextvars.copy_context()
    var.set('Беги быстрее, дракон на хвосте!')
    content_2 = contextvars.copy_context()

    treasure_hunt = asyncio.create_task(
        countdown(name='Квест на поиск сокровищ', seconds=10),
        context=content_1
    )
    dragon_escape = asyncio.create_task(
        countdown(name='Побег от дракона', seconds=5),
        context=content_2
    )
    await asyncio.gather(treasure_hunt, dragon_escape)


if __name__ == "__main__":
    asyncio.run(main())
