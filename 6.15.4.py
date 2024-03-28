import asyncio


async def publish_post(text: str) -> str:
    await asyncio.sleep(1)
    string = f'Пост опубликован: {text}'
    print(string)
    return string


async def notify_subscribers(subscribers: list[str]) -> None:
    for subscriber in subscribers:
        await asyncio.sleep(1)
        print(f'Уведомление отправлено {subscriber}')


async def main():
    post_text = "Hello world!"
    subscribers = ["Alice", "Bob", "Charlie", "Dave", "Emma", "Frank", "Grace", "Henry", "Isabella", "Jack"]
    await asyncio.gather(publish_post(post_text), notify_subscribers(subscribers))


if __name__ == '__main__':
    asyncio.run(main())
