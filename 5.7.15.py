import asyncio
from typing import Any

from data import data


async def check_access(participant: dict[str, Any]) -> None:
    await asyncio.sleep(participant.get('Уровень секретности'))
    if participant.get('Срок доступа'):
        print(f'Участник {asyncio.current_task().get_name()} имеет действующий доступ. '
              f'Продолжительность доступа: {participant.get("Срок доступа")}')
    else:
        print(f'Ошибка доступа: У участника {asyncio.current_task().get_name()} '
              f'срок доступа истек или не указан.')
        raise ValueError


async def main() -> None:
    tasks = [
        asyncio.create_task(check_access(participant), name=f'{participant.get("Имя")} {participant.get("Фамилия")}'
                            ) for participant in data
    ]
    _, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
    for task in pending:
        task.cancel()
        print(f'Доступ участника {task.get_name()} отменен из-за критической ошибки.')


if __name__ == '__main__':
    asyncio.run(main())
