# Создать базу данных для хранения информации о студентах университета.
# База данных должна содержать две таблицы: "Студенты" и "Факультеты".
# В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, возраст, пол, группа и id факультета.
# В таблице "Факультеты" должны быть следующие поля: id и название факультета.
# Необходимо создать связь между таблицами "Студенты" и "Факультеты".
# Написать функцию-обработчик, которая будет выводить список всех студентов с указанием их факультета.
import random

from flask import Flask, render_template
from Lesson3.model1 import db, Students, Faculties

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.route('/')
@app.route('/students/')
def all_students():
    students = Students.query.all()
    context = {'students': students}
    return render_template('table.html', **context)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('Таблицы созданы')


@app.cli.command("fill-db")
def fill_tables():
    cnt = 5

    f = ['Philology', 'Psychology', 'Economics', 'Ecology', 'Artificial Intelligence']
    for i in range(cnt):
        faculty = Faculties(name=f'{f[i]}')
        db.session.add(faculty)
    db.session.commit()

    for i in range(1, cnt * 5 + 1):
        student = Students(name=f'Name_{i}',
                           last_name=f'LastName_{i}',
                           age=f'{random.randint(18, 25)}',
                           group_=f'{random.randint(1, 5)}',
                           faculty_id=f'{i % cnt + 1}')
        db.session.add(student)
    db.session.commit()
    print('Таблицы заполнены')
