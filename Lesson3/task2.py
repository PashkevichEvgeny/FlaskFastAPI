# Создать базу данных для хранения информации о книгах в библиотеке.
# База данных должна содержать две таблицы: "Книги" и "Авторы".
# В таблице "Книги" должны быть следующие поля: id, название, год издания, количество экземпляров и id автора.
# В таблице "Авторы" должны быть следующие поля: id, имя и фамилия.
# Необходимо создать связь между таблицами "Книги" и "Авторы".
# Написать функцию-обработчик, которая будет выводить список всех книг с указанием их авторов.
import random

from flask import Flask, render_template
from Lesson3.model_book import db, Authors, Books

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


@app.route('/')
@app.route('/books/')
def all_books():
    books = Books.query.all()
    context = {'books': books}
    return render_template('book.html', **context)


@app.cli.command("fill-db")
def fill_tables():
    db.create_all()
    print('База создана')

    cnt = 5

    for i in range(cnt):
        authors = Authors(name=f'Name_{i}', last_name=f'LastName{i}')
        db.session.add(authors)
    db.session.commit()

    for i in range(1, cnt * 5 + 1):
        books = Books(title=f'Title_{i}',
                      year=f'{random.randint(2000, 2023)}',
                      amount=f'{random.randint(1, 5)}',
                      author_id=f'{i % cnt + 1}')
        db.session.add(books)
    db.session.commit()
    print('Таблицы заполнены')
