import asyncio

books_json = [
    {
        "Порядковый номер": 1,
        "Автор": "Rebecca Butler",
        "Название": "Three point south wear score organization.",
        "Год издания": "1985",
        "Наличие на полке": True
    },
    {
        "Порядковый номер": 2,
        "Автор": "Mark Cole",
        "Название": "Drive experience customer somebody pressure.",
        "Год издания": "1985",
        "Наличие на полке": True
    },
]


async def check_book(book: dict[str, any]) -> str | None:
    await asyncio.sleep(0)
    if not book.get('Наличие на полке'):
        return (f'{book.get("Порядковый номер")}: '
                f'{book.get("Автор")}: '
                f'{book.get("Название")} '
                f'({book.get("Год издания")})')


async def main() -> None:
    coros = (check_book(book) for book in books_json)
    results = await asyncio.gather(*coros)
    print(
        *(tmp for result in results if (tmp := result) is not None), sep='\n'
    )


if __name__ == '__main__':
    asyncio.run(main())
