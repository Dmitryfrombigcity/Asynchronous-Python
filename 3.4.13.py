import asyncio


async def coro_1():
    print('coro_1 says, hello coro_2!')


async def coro_2():
    print('coro_2 says, hello coro_1!')


async def main():

    # New in version 3.11
    # async with asyncio.TaskGroup() as group:
    #     first = group.create_task(coro_1())
    #     second = group.create_task(coro_2())

    await asyncio.gather(coro_1(), coro_2())

if __name__ == '__main__':
    asyncio.run(main())
