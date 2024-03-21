import asyncio


async def activate_portal(x: float = 2) -> float:
    print(f'Активация портала в процессе, требуется времени: {x} единиц')
    await asyncio.sleep(x)
    return x * 2


async def perform_teleportation(x: float) -> float:
    print(f'Телепортация в процессе, требуется времени: {x} единиц')
    await asyncio.sleep(x)
    return x + 2


async def portal_operator() -> None:
    result_1 = await asyncio.ensure_future(activate_portal())
    result_2 = await asyncio.ensure_future(perform_teleportation(1)) if result_1 > 4 else \
        await asyncio.ensure_future(perform_teleportation(result_1))
    print(
        f'Результат активации портала: {result_1} единиц энергии\n'
        f'Результат телепортации: {result_2} единиц времени'
    )


if __name__ == '__main__':
    asyncio.run(portal_operator())
