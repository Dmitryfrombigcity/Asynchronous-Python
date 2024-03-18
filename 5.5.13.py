import asyncio

spells = {
    "Огненный шар": 7,
    "Ледяная стрела": 2,
    "Щит молний": 6,
}

max_cast_time = 5

students = [
    "Алара",
    "Бренн",
    "Сирил",
    "Дариа",
    "Элвин"
]


async def cast_spell(
        student: str,
        spell: str,
        cast_time: float
) -> None:
    await asyncio.sleep(cast_time)
    if cast_time <= max_cast_time:
        print(f'{student} успешно кастует {spell} за {cast_time} сек.')
    else:
        print(f'Ученик {student} не справился с заклинанием {spell}, и учитель применил щит.'
              f' {student} успешно завершает заклинание с помощью shield.')


async def main() -> None:
    coros = (
        (asyncio.shield(cast_spell(student, spell, cast_time))) for student in students
        for spell, cast_time in spells.items()
    )
    try:
        await asyncio.wait_for(asyncio.gather(*coros), timeout=max_cast_time)
    except asyncio.TimeoutError:
        # task_main = asyncio.current_task()
        # tasks = asyncio.all_tasks()
        # tasks.remove(task_main)
        # print(*tasks, sep='\n')
        # await asyncio.gather(*tasks)
        while len(asyncio.all_tasks()) > 1:
            await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(main())
