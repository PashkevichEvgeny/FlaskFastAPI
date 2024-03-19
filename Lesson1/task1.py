# Напишите простое веб-приложение на Flask, которое будет выводить на экран текст "Hello, World!"

# Запуск из терминала
# C:\pycharm\FlaskFastAPI> flask --app .\Lesson1\task1.py run --debug

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world() -> str:
    return 'Hello World!!!'


if __name__ == '__main__':
    app.run()
