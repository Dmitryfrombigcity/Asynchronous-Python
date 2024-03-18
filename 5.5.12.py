import asyncio

runners = {
    "Молния Марк": 2.8,
    "Ветренный Виктор": 13.5,
    "Скоростной Степан": 11.2,
    "Быстрая Белла": 10.8,
}
lst: list[str] = []


async def run_lap(name: str, speed: float, distance: float = 100):
    time = round(distance / speed, 2)
    await asyncio.sleep(time)
    # return f'{name} завершил круг за {time} секунд'
    lst.append(f'{name} завершил круг за {time} секунд')

async def main(max_time: float = 10):
    coros = (asyncio.wait_for(
        run_lap(name, speed), max_time) for name, speed in runners.items()
    )
    res = await asyncio.gather(*coros, return_exceptions=True)
    # результат в порядке постановки в цикл
    # print(*filter(lambda x: isinstance(x, str), res), sep='\n')
    # результат в порядке выполнения корутин
    print(*lst, sep='\n')


if __name__ == '__main__':
    asyncio.run(main())
