import asyncio

wood_resources_dict = {
    'Деревянный меч': 6,
    'Деревянный щит': 12,
    'Деревянный стул': 24,
}


async def gather_wood(condition: asyncio.Condition, storage: int = 0):
    for value in wood_resources_dict.values():

        while True:
            await asyncio.sleep(1)
            storage += 2
            print(f"Добыто 2 ед. дерева. На складе {storage} ед.")
            async with condition:
                if value <= storage:
                    condition.notify()
                    storage -= value
                    break


async def craft_item(condition: asyncio.Condition):
    for key in wood_resources_dict.keys():
        async with condition:
            await condition.wait()
            print(f"Изготовлен {key}.")


async def main():
    condition = asyncio.Condition()
    await asyncio.gather(gather_wood(condition), craft_item(condition))


if __name__ == '__main__':
    asyncio.run(main())
