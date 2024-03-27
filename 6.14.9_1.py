import asyncio


class TaskGroupReturn(asyncio.TaskGroup):
    def __init__(self):
        super().__init__()
        self.results = {}

    async def __aexit__(self, et, exc, tb):
        self.results = self._tasks.copy()
        await super().__aexit__(et, exc, tb)


async def file_reader(filename: str) -> str:
    """Корутина для чтения файла"""
    with open(filename) as f:
        data: str = f.read()
    return data


async def get_data(data: int) -> dict:
    """Корутина, для возврата переданного числа в виде словаря вида {'data': data}"""
    if data == 0:
        raise Exception('Нет данных...')
    return {'data': data}


async def main():
    try:
        async with TaskGroupReturn() as tg:
            task1 = tg.create_task(get_data(1))
            task2 = tg.create_task(get_data(2))
            task3 = tg.create_task(get_data(0))
            task4 = tg.create_task(file_reader('fake.png'))
            task5 = tg.create_task(file_reader('new_fake.png'))
            task6 = tg.create_task(get_data(0))
    except* FileNotFoundError as e:
        for error in e.exceptions:
            print(error)
    except* Exception as e:
        for error in e.exceptions:
            print(error)
    finally:
        print('---------------РЕЗУЛЬТАТЫ + ОШИБКИ-----------------')
        for task in tg.results:
            if task.exception():
                print(f'Исключение {task.get_name()}: {task.exception()}')
            else:
                print(f'Результат {task.get_name()}: {task.result()}')

if __name__ == '__main__':
    asyncio.run(main())
