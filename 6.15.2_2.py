import asyncio
from random import randrange, randint


async def scan_port(
        address: str,
        port: int
) -> int:
    await asyncio.sleep(randrange(1, 10))
    if randint(0, 1):
        print(f'Порт {port} на адресе {address} открыт')
        return port


async def scan_range(
        address: str,
        start_port: int,
        end_port: int
) -> None:
    print(f'Сканирование портов с {start_port} по {end_port} на адресе {address}')
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(
            scan_port(address, port)) for port in range(start_port, end_port + 1)
        ]
    open_ports = [port for task in tasks if (port := task.result()) is not None]
    if open_ports:
        print(f'Открытые порты на адресе {address}: {open_ports}')
    else:
        print(f'Открытых портов на адресе {address} не найдено')


if __name__ == '__main__':
    address = '192.168.0.1'
    start_port = 80
    end_port = 85
    asyncio.run(scan_range(address, start_port, end_port))
