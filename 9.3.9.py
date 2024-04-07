import asyncio
from random import randrange


async def get_alarm(alarm: asyncio.Event) -> None:
    await asyncio.sleep(randrange(6))
    alarm.set()
    print('Датчики зафиксировали движение')


async def sensor(
        number: int,
        address: str,
        alarm: asyncio.Event
) -> None:
    print(f'Датчик {number} IP-адрес {address} настроен и ожидает срабатывания')
    await alarm.wait()
    print(f'Датчик {number} IP-адрес {address} активирован, "Wee-wee-wee-wee"')


async def main():
    alarm = asyncio.Event()
    ip = ["192.168.0.3", "192.168.0.1", "192.168.0.2", "192.168.0.4", "192.168.0.5"]
    event = asyncio.create_task(get_alarm(alarm))
    await asyncio.gather(*(sensor(ind, address, alarm) for ind, address in enumerate(ip)))


if __name__ == '__main__':
    asyncio.run(main())
