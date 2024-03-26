import asyncio
from contextvars import ContextVar, copy_context

var = ContextVar('var')

codes = [
    "56FF4D", "A3D2F7", "B1C94E", "F56A1D", "D4E6F1",
    "A1B2C3", "D4E5F6", "A7B8C9", "D0E1F2", "A3B4C5",
    "D6E7F8", "A9B0C1", "D2E3F4", "A5B6C7", "D8E9F0"
]

messages = [
    "Привет, мир!", "Как дела?", "Что нового?", "Добрый день!", "Пока!",
    "Спокойной ночи!", "Удачного дня!", "Всего хорошего!", "До встречи!", "Счастливого пути!",
    "Успехов в работе!", "Приятного аппетита!", "Хорошего настроения!", "Спасибо за помощь!",
    "Всего наилучшего!"
]


def get_code(task) -> None:
    print(f'''{task.result()}
Код: {var.get()}''')


async def coro(message: str) -> str:
    return f'Сообщение: {message}'


async def main():
    tasks = [asyncio.create_task(coro(message)) for message in messages]
    for task, code in zip(tasks, codes):
        var.set(code)
        ctx = copy_context()
        task.add_done_callback(get_code, context=ctx)
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
