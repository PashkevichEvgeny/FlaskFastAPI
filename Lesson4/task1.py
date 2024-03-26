# Написать программу, которая считывает список из 10 URL адресов и одновременно загружает данные с каждого адреса.
# После загрузки данных нужно записать их в отдельные файлы.
# Используйте потоки.
from os.path import join as join_path

import requests
import threading
import time
from url_storage import urls


def download(url):
    response = requests.get(url)
    path = 'downloads'
    filename = f"threading_{url.replace('https://', '').replace('.', '_').replace('/', '')} .html"
    with open(f'{join_path(path, filename)}', "w", encoding='utf-8') as f:
        f.write(response.text)
        print(f"Downloaded {url} in {time.time()-start_time:.2f} seconds")


threads = []
start_time = time.time()

if __name__ == '__main__':
    for url in urls:
        thread = threading.Thread(target=download, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
