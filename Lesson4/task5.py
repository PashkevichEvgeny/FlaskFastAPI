# Создать программу, которая будет производить подсчет количества слов в каждом файле в указанной директории
# и выводить результаты в консоль.
# Используйте процессы.

from multiprocessing import Process
import time
from pathlib import Path


def count_word_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        cnt = 0
        for word in f.readlines():
            cnt += len(word.split())
        # do some processing with the file contents
        print(f'{f.name} содержит {cnt} слов.')


def main():
    dir_path = Path('.')
    processes = []

    file_paths = [file_path for file_path in dir_path.iterdir() if file_path.is_file()]
    for file in file_paths:
        process = Process(target=count_word_in_file, args=(file,))
        processes.append(process)
        process.start()
        print(f'{process.name} Выполнено за {time.time() - start_time:.2f} сек.')

    for process in processes:
        process.join()


start_time = time.time()

if __name__ == '__main__':
    main()
