# Написать программу, которая считывает список из 10 URL адресов и одновременно загружает данные с каждого адреса.
# После загрузки данных нужно записать их в отдельные файлы.
# Используйте процессы.
from os.path import join as join_path

import requests
from multiprocessing import Process
import time
from url_storage import urls


def download(url):
    response = requests.get(url)
    path = 'downloads'
    filename = 'multiprocessing_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    with open(f'{join_path(path, filename)}', "w", encoding='utf-8') as f:
        f.write(response.text)
        print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


processes = []
start_time = time.time()

if __name__ == '__main__':
    for url in urls:
        process = Process(target=download, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
