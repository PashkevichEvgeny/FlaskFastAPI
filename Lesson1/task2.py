# Добавьте две дополнительные страницы в ваше вебприложение: страницу "about", страницу "contact"

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world() -> str:
    return 'Hello World!!!'


@app.route('/about/')
def about_page() -> str:
    return 'Это тестовый сервер для изучения фреймворка Flask.'


@app.route('/contact/')
def contact_page() -> str:
    return 'Для контакта используйте e-mail: @gmail.com'
