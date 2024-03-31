# Создать API для добавления нового пользователя в базу данных. Приложение
# должно иметь возможность принимать POST запросы с данными нового
# пользователя и сохранять их в базу данных.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для добавления нового пользователя (метод POST).
# Реализуйте валидацию данных запроса и ответа.

from fastapi import FastAPI

from Lesson5.db import curs, conn
from Lesson5.model_user import User

app = FastAPI()


curs.execute("""Create table if not exists user(
                user_id integer not null primary key,
                name text,
                email text,
                password)""")


def get_one(user_id: int) -> User:
    qry = "select * from user where user_id=:user_id"
    params = {"user_id": user_id}
    curs.execute(qry, params)
    id_, name, email, password = curs.fetchone()
    return User(user_id=id_, name=name, email=email, password=password)


def create(user: User) -> User:
    qry = "insert into user values (:user_id, :name, :email, :password)"
    params = user.dict()
    curs.execute(qry, params)
    conn.commit()
    return user


users = []


@app.post('/add-user/')
async def add_user(user: User):
    create(user)
    users.append(user)
    return {'User': user}


@app.get('/get/all/')
async def get_all():
    qry = "select * from user"
    curs.execute(qry)
    return [row for row in curs.fetchall()]


@app.get('/get/{user_id}')
async def get_user(user_id: int):
    user = get_one(user_id)
    return {'user': user}


