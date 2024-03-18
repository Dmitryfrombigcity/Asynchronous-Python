import asyncio

places = [
    "начинает путешествие",
    "находит загадочный лес",
    "переправляется через реку",
    "встречает дружелюбного дракона",
    "находит сокровище"
]

roles = [
    "Искатель приключений",
    "Храбрый рыцарь",
    "Отважный пират"
]


async def counter(
        name: str,
        delay: int = 1
) -> None:
    for place in places:
        print(f'{name} {place}...')
        await asyncio.sleep(delay)


async def main():
    await asyncio.gather(*(counter(item) for item in roles))


if __name__ == "__main__":
    asyncio.run(main())
