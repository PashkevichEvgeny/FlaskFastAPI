# Создать базовый шаблон для всего сайта, содержащий общие элементы дизайна (шапка, меню, подвал),
# и дочерние шаблоны для каждой отдельной страницы.
# Например, создать страницу "О нас" и "Контакты", используя базовый шаблон.
import csv
import datetime
import os

from flask import Flask, render_template

app = Flask(__name__)


def path_file(name):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/news/', name)


@app.route('/')
@app.route('/main/')
def main(path='/main'):
    context = {'title': 'Главная', 'name': 'Котофей'}
    return render_template('main.html', **context)


@app.route('/new-table/')
def table_page():
    table_title = ['Имя', 'Фамилия', 'Возраст', 'Средний балл']
    students = [{'name': 'Котофей', 'last_name': 'Котофеевич', 'age': '18', 'gpa': '80'},
                {'name': 'Дорофей', 'last_name': 'Дорофеевич', 'age': '19', 'gpa': '71'},
                {'name': 'Тимофей', 'last_name': 'Тимоофеевич', 'age': '18', 'gpa': '93'},
                {'name': 'Ерофей', 'last_name': 'Ерофеевич', 'age': '19', 'gpa': '85'},
                ]
    context = {'title': 'Таблица успеваемости', 'students': students, 'table_title': table_title}
    return render_template('new_table.html', **context)


@app.route('/new-news/')
def news_page():
    with open(path_file('news.csv'), 'r', encoding='UTF-8') as f:
        # news = csv.DictReader(f, fieldnames=['title', 'review'])
        news = [{'title': title, 'review': review, 'date': datetime.datetime.now().strftime('%d-%m-%y')}
                for title, review in csv.reader(f, delimiter="|")]
    context = {'title': 'Новости', 'news': news}
    return render_template('new_news.html', **context)
