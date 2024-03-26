# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
# Каждое изображение должно сохраняться в отдельном файле,
# название которого соответствует названию изображения в URL-адресе.
#   Например URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# Программа должна выводить в консоль информацию о времени скачивания каждого изображения
# и общем времени выполнения программы.
import argparse
from os.path import join as join_path, split as split_path
import threading
from multiprocessing import Process
from time import time
import asyncio
import aiohttp
import aiofiles
import requests


def download(url, prefix):
    """Загрузчик для многопотокового и многопроцессорного решения"""
    start_time = time()
    response = requests.get(url)
    path = 'downloads'
    filename = f"{prefix}_{split_path(url)[1]}"
    with open(f'{join_path(path, filename)}', "wb") as f:
        f.write(response.content)
        print(f'Downloaded {url} in {time() - start_time:.2f} seconds')


def threads_main():
    """ Многопоточное решение"""
    treads_time = time()
    threads = []
    for image in images:
        thread = threading.Thread(target=download, args=(image, 'threading'))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print(f'Многопотоковая загрузка завершена {time() - treads_time:.2f} seconds')


def processes_main():
    """Многопроцессорное решение"""
    proc_time = time()
    processes = []
    for image in images:
        process = Process(target=download, args=(image, 'process'))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    print(f'Многопроцессорная загрузка завершена {time() - proc_time:.2f} seconds')


async def async_download(url, prefix):
    """Асинхронный загрузчик"""
    # асинхронная загрузка картинки из сети
    async_time = time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                picture = await response.content.read()
    # асинхронная запись картинки в файл
    path, filename = 'downloads', f'{prefix}_{split_path(url)[1]}'
    async with aiofiles.open(f'{join_path(path, filename)}', "wb") as f:
        await f.write(picture)
    print(f'Downloaded {url} in {time() - async_time:.2f} seconds')


async def async_main():
    """Асинхронное решение"""
    start_time = time()
    tasks = []
    for image in images:
        task = asyncio.create_task(async_download(image, 'async'))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f'Асинхронная загрузка завершена {time() - start_time:.2f} seconds')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Picture downloader')
    parser.add_argument('list_link', metavar='ListLink', type=str, nargs='*', help='enter link to download')
    images = parser.parse_args().list_link

    threads_main()

    processes_main()

    asyncio.run(async_main())

    # python task9.py https://cs13.pikabu.ru/post_img/2024/03/26/7/1711449302152420184.jpg https://cs14.pikabu.ru/post_img/2024/03/26/5/1711433979159113373.jpg https://cs14.pikabu.ru/post_img/2024/03/26/1/1711404099150111622.jpg
