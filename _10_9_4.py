import asyncio
import io
import zipfile
from time import perf_counter

import requests

# https://github.com/Dmitryfrombigcity/Asynchronous-Python/blob/master/_10_9_1.py
from _10_9_1 import send_result
from _10_9_3 import main

if __name__ == '__main__':
    start = perf_counter()
    stepic = 'https://stepik.org/lesson/1029069/step/4?unit=1037339'
    url = 'https://parsinger.ru/asyncio_course/5000folder.zip'
    sub_dir = '10_9_4'
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zf:
        zf.extractall(path=sub_dir)

    result = asyncio.run(main(sub_dir))

    print(perf_counter() - start)
    send_result(result, stepic)
