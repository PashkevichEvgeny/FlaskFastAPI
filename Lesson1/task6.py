""" Написать функцию, которая будет выводить на экран HTML страницу с таблицей, содержащей информацию о студентах.
Таблица должна содержать следующие поля: "Имя", "Фамилия", "Возраст", "Средний балл".
Данные о студентах должны быть переданы в шаблон через контекст. """

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return '<a href="index">Hello!</a> ' \
           '<a href="index2">Hello context</a></br>' \
           '<a href="table">Table</a>'


@app.route('/index/')
def html_index():
    return render_template('index.html')


@app.route('/index2/')
def html_index2():
    context = {
        'title': 'Личный блог',
        'name': 'Котофей Котофеевич'
    }
    return render_template('index2.html', **context)


@app.route('/table/')
def html_table():
    table_title = ['Имя', 'Фамилия', 'Возраст','Средний балл']
    students = [{'name': 'Котофей', 'last_name': 'Котофеевич', 'age': '18', 'gpa': '80'},
                {'name': 'Дорофей', 'last_name': 'Дорофеевич', 'age': '19', 'gpa': '71'},
                {'name': 'Тимофей', 'last_name': 'Тимоофеевич', 'age': '18', 'gpa': '93'},
                {'name': 'Ерофей', 'last_name': 'Ерофеевич', 'age': '19', 'gpa': '85'},
                ]
    context = {'students': students, 'table_title': table_title}
    return render_template('table.html', **context)

