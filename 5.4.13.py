import asyncio


async def monitor(status_list: list[str]) -> None:
    lst = status_list[:]
    task_name = asyncio.current_task().get_name()
    for status in lst:
        print(f"[{task_name}] Статус проверки: {status}")
        if status == "Катастрофически":
            print(f"[{task_name}] Критическое состояние достигнуто. Инициируется остановка...")
        await asyncio.sleep(0)


async def main():
    status_list = [
        "Отлично", "Хорошо", "Удовлетворительно", "Средне",
        "Пониженное", "Ниже среднего", "Плохо", "Очень плохо",
        "Критично", "Катастрофически"
    ]
    tasks = (asyncio.create_task(monitor(status_list), name=name) for name in
             ("CPU", "Память", "Дисковое пространство")
             )
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
