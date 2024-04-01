import asyncio
from itertools import product
from random import randint

shapes = ["circle", "star", "square", "diamond", "heart"]
colors = ["red", "blue", "green", "yellow", "purple"]
actions = ["change_color", "explode", "disappear"]


async def launch_firework(combination: tuple[str, str, str]) -> None:
    shape, color, action = combination
    print(f"Запущен {color} {shape} салют, в форме {action}!!!")
    await asyncio.sleep(randint(1, 5))
    print(f"Салют {color} {shape} завершил выступление {action}")


async def main() -> None:
    combinations = list(product(shapes, colors, actions))
    print(combinations)
    await asyncio.gather(*(launch_firework(combination) for combination in combinations))


if __name__ == '__main__':
    asyncio.run(main())
