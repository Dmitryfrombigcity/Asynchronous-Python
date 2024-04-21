import asyncio
from time import sleep

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from environs import Env
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


async def main() -> str:
    code_dict = {
        0: 'F',
        1: 'B',
        2: 'D',
        3: 'J',
        4: 'E',
        5: 'C',
        6: 'H',
        7: 'G',
        8: 'A',
        9: 'I'
    }
    async with ClientSession() as session, session.get(url) as response:
        content = await response.text()
    soup = BeautifulSoup(content, 'lxml')
    text = (code_dict[int(item)] for item in soup.find('p').text.strip())
    return ''.join(text)


def send_result(
        result: str,
        stepic: str
) -> None:
    env = Env()
    env.read_env(recurse=False)
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')

    with webdriver.Chrome(options=options) as driver:
        wait = WebDriverWait(driver, 15)
        driver.get(stepic)
        driver.add_cookie({'name': 'sessionid', 'value': env('STEPIK_SESSIONID')})
        driver.refresh()
        wait.until(
            ec.visibility_of_element_located(('xpath', '//div[@class="attempt"]//textarea'))
        ).send_keys(result)
        wait.until(
            ec.element_to_be_clickable(('xpath', '//button[@class="submit-submission"]'))
        ).click()
        sleep(1)


if __name__ == '__main__':
    stepic = 'https://stepik.org/lesson/1075354/step/2?unit=1085452'
    url = 'https://asyncio.ru/zadachi/1/index.html'
    send_result(asyncio.run(main()), stepic)
