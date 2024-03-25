# Доработаем задача про студентов
# Создать базу данных для хранения информации о студентах и их оценках в учебном заведении.
# База данных должна содержать две таблицы: "Студенты" и "Оценки".
# В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, группа и email.
# В таблице "Оценки" должны быть следующие поля: id, id студента, название предмета и оценка.
# Необходимо создать связь между таблицами "Студенты" и "Оценки".
# Написать функцию-обработчик, которая будет выводить список всех студентов с указанием их оценок.
import random

from flask import Flask, render_template
from Lesson3.model_student2 import db, Students2, Grades

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.route('/')
@app.route('/students/')
def all_books():
    students = Students2.query.all()
    context = {'students': students}
    return render_template('table2.html', **context)


@app.cli.command("fill-db")
def fill_tables():
    db.drop_all()
    db.create_all()
    print('Таблицы созданы')

    cnt = 5

    for i in range(1, cnt + 1):
        students = Students2(name=f'Name_{i}',
                             last_name=f'LastName{i}',
                             group_=f'{random.randint(1, 5)}',
                             email=f'abc{i}@gmail.com')
        db.session.add(students)
    db.session.commit()

    f = ['Philology', 'Psychology', 'Economics', 'Ecology', 'Artificial Intelligence']
    for i in range(cnt * 5):
        grades = Grades(student_id=f'{i % cnt + 1}',
                        name_subject=f'{f[i // cnt]}',
                        grade=f'{random.randint(1, 5)}')
        db.session.add(grades)
    db.session.commit()
    print('Таблицы заполнены')

