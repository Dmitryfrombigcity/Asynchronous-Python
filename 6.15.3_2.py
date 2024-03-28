import asyncio
import random


async def scan_port(
        address: str,
        port: int
) -> int | None:
    """
    Асинхронная функция, имитирующая сканирование порта на заданном ip-адресе.
    """
    await asyncio.sleep(1)
    if random.randint(0, 100) == 1:
        print(f'Port {port} on {address} is open')
        return port


async def scan_range(
        address: str,
        start_port: int,
        end_port: int
) -> tuple[str, list[int]]:
    """
    Асинхронная функция, проверяющая состояние диапазона портов по указанному адресу.
    """
    print(f'Scanning ports {start_port}-{end_port} on {address}')
    async with asyncio.TaskGroup() as group:
        tasks = [
            group.create_task(scan_port(address, port)) for port in range(start_port, end_port + 1)
        ]
    open_ports = [port for task in tasks if (port := task.result()) is not None]
    return address, open_ports


async def main(
        dct: dict[str, list[int]]
) -> None:
    """
    Основная асинхронная функция, управляющая процессом сканирования портов из словаря dct.
    """
    async with asyncio.TaskGroup() as group:
        tasks = [
            group.create_task(scan_range(address, ports[0], ports[-1])) for address, ports in dct.items()
        ]
    for task in tasks:
        result = task.result()
        if len(result[-1]):
            print(f'Всего найдено открытых портов {len(result[-1])} {result[-1]} '
                  f'для ip: {result[0]}')


if __name__ == '__main__':
    ip_dct = {
        '192.168.0.1': [0, 100],
        '192.168.0.2': [225, 300],
        '192.168.2.5': [150, 185]
    }
    asyncio.run(main(ip_dct))
