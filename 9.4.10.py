import asyncio
from typing import Any


async def gather(
        condition: asyncio.Condition,
        material_dict: dict,
        material: str,
        items_per_hour: int,
        storage: int = 0
) -> None:
    for value in material_dict.values():
        while True:
            await asyncio.sleep(1)
            storage += items_per_hour
            print(f'Добыто {items_per_hour} ед. {material}. На складе {storage} ед.')
            async with condition:
                if value <= storage:
                    condition.notify()
                    storage -= value
                    break


async def craft(
        condition: asyncio.Condition,
        material_dict: dict,
        material: str,
        *args: Any
) -> None:
    for key in material_dict.keys():
        async with condition:
            await condition.wait()
            print(f"Изготовлен {key} из {material}.")


async def main():
    stone_resources_dict = {
        'Каменная плитка': 10,
        'Каменная ваза': 40,
        'Каменный столб': 50,
    }

    metal_resources_dict = {
        'Металлическая цепь': 6,
        'Металлическая рамка': 24,
        'Металлическая ручка': 54,
    }

    cloth_resources_dict = {
        'Тканевая занавеска': 8,
        'Тканевый чехол': 24,
        'Тканевое покрывало': 48,
    }
    stone = (asyncio.Condition(), stone_resources_dict, 'камня', 10)
    metal = (asyncio.Condition(), metal_resources_dict, 'металла', 6)
    cloth = (asyncio.Condition(), cloth_resources_dict, 'ткани', 8)
    await asyncio.gather(
        gather(*stone), gather(*metal), gather(*cloth),
        craft(*stone), craft(*metal), craft(*cloth)
    )


if __name__ == '__main__':
    asyncio.run(main())
