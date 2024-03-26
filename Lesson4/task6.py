# Создать программу, которая будет производить подсчет количества слов в каждом файле в указанной директории
# и выводить результаты в консоль.
# Используйте асинхронный подход.

import asyncio
import time
from pathlib import Path


async def count_word_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        cnt = 0
        for word in f.readlines():
            cnt += len(word.split())
        # do some processing with the file contents
        print(f'{f.name} содержит {cnt} слов. Выполнено за {time.time() - start_time:.2f} сек.')


async def main():
    dir_path = Path('.')
    file_paths = [file_path for file_path in dir_path.iterdir() if file_path.is_file()]
    tasks = [asyncio.create_task(count_word_in_file(file_path)) for file_path in file_paths]
    await asyncio.gather(*tasks)


start_time = time.time()

if __name__ == '__main__':
    asyncio.run(main())
