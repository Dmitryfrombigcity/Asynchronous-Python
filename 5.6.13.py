import asyncio

equipment_list = ['#001 ps5f6537c5-506f-43c2-b095-1890ef579c52: 265 units',
                  '#002 ps5ec3020b-022f-466b-845a-a8f11161a6d1: 39 units',
                  '#003 psb5c6c090-4f1a-4741-936e-5fe2b3e8d181: 242 units',
                  '#004 ps10c90127-a4a5-4f85-b23f-66421ab04b09: 108 units',
                  '#005 psa8b77d97-ef82-4832-9601-36abfc399af2: 72 units']


def query_time() -> float:
    return 1.009015


async def equipment_request(request: str) -> str:
    await asyncio.sleep(1)
    return f'{request[:4]} is Ok!'


async def send_requests() -> None:
    coros = map(equipment_request, equipment_list)
    await asyncio.gather(*coros)
    print(f'На отправку {len(equipment_list)} запросов потребовалось {query_time()} секунд!')


if __name__ == '__main__':
    asyncio.run(send_requests())
