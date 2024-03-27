import asyncio


class TaskGroupReturn(asyncio.TaskGroup):

    # ... the minimal coding to get the forgiveful task group can be achieved by neutering its internal _abort method.
    # This method is called on task exception handling, and all it does is loop through all tasks not yet done and
    # cancel them. Tasks not cancelled would still be awaited at the end of the with block -
    # and that is what we get by preventing _abort from running.
    # https://stackoverflow.com/questions/75250788/how-to-prevent-python3-11-taskgroup-from-canceling-all-the-tasks
    #
    def _abort(self):
        ...


async def file_reader(filename: str) -> str:
    """Корутина для чтения файла"""
    with open(filename) as f:
        data: str = f.read()
    return data


async def get_data(data: int) -> dict:
    """Корутина, для возврата переданного числа в виде словаря вида {'data': data}"""
    await asyncio.sleep(1)
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
        result = [task1, task2, task3, task4, task5, task6]
        for task in result:
            if task.exception():
                print(f'Исключение {task.get_name()}: {task.exception()}')
            else:
                print(f'Результат {task.get_name()}: {task.result()}')


if __name__ == '__main__':
    asyncio.run(main())
