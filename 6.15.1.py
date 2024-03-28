import asyncio
from random import randint

server_names = {
    "1": "Server_Alpha", "2": "Server_Beta", "3": "Server_Gamma",
    "4": "Server_Delta", "5": "Server_Epsilon"
}


async def load_data(server):
    print(f'Загрузка данных с сервера {server} началась')
    await asyncio.sleep(randint(0, 5))
    print(f'Загрузка данных с сервера {server} завершена')


async def main(n):
    tasks = (load_data(server) for server in tuple(server_names.values())[:n])
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main(5))
