import asyncio


async def activate_portal(x: float = 2) -> float:
    print(f'Активация портала в процессе, требуется времени: {x} единиц')
    await asyncio.sleep(x)
    return x * 2


async def perform_teleportation(x: float = 3) -> float:
    print(f'Телепортация в процессе, требуется времени: {x} единиц')
    await asyncio.sleep(x)
    return x + 2


async def recharge_portal(x: float = 4) -> float:
    print(f'Подзарядка портала, требуется времени: {x} единиц')
    await asyncio.sleep(x)
    return x * 3


async def check_portal_stability(x: float = 5) -> float:
    print(f'Проверка стабильности портала, требуется времени: {x} единиц')
    await asyncio.sleep(x)
    return x + 4


async def restore_portal(x: float = 6) -> float:
    print(f'Восстановление портала, требуется времени: {x} единиц')
    await asyncio.sleep(x)
    return x * 5


async def close_portal(x: float = 7) -> float:
    print(f'Закрытие портала, требуется времени: {x} единиц')
    await asyncio.sleep(x)
    return x - 1


async def portal_operator() -> None:
    tasks = (
        asyncio.ensure_future(activate_portal()),
        asyncio.ensure_future(perform_teleportation()),
        asyncio.ensure_future(recharge_portal()),
        asyncio.ensure_future(check_portal_stability()),
        asyncio.ensure_future(restore_portal()),
        asyncio.ensure_future(close_portal())
    )

    res_1, res_2, res_3, res_4, res_5, res_6 = await asyncio.gather(*tasks)

    print(f'''Результат активации портала: {res_1} единиц энергии
Результат телепортации: {res_2} единиц времени
Результат подзарядки портала: {res_3} единиц энергии
Результат проверки стабильности: {res_4} единиц времени
Результат восстановления портала: {res_5} единиц энергии
Результат закрытия портала: {res_6} единиц времени
''')


if __name__ == '__main__':
    asyncio.run(portal_operator())
