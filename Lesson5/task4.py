# Создать API для обновления информации о пользователе в базе данных.
# Приложение должно иметь возможность принимать PUT запросы с данными
# пользователей и обновлять их в базе данных.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для обновления информации о пользователе (метод PUT).
# Реализуйте валидацию данных запроса и ответа.

from fastapi import FastAPI
from pydantic import EmailStr

from Lesson5.db import curs, conn
from Lesson5.model_user import User

app = FastAPI()


def get_one(user_id: int) -> User:
    qry = "select * from user where user_id=:user_id"
    params = {"user_id": user_id}
    curs.execute(qry, params)
    id_, name, email, password = curs.fetchone()
    return User(user_id=id_, name=name, email=email, password=password)


def modify(user_id: int, user: User) -> User:
    qry = """update user
             set 
                 user_id=:user_id,
                 name=:name,
                 email=:email
             where 
                 user_id=:seek_id"""
    params = user.model_dump()
    params['seek_id'] = user_id
    curs.execute(qry, params)
    conn.commit()
    return user


@app.put('/user/edit/{user_id}')
async def update(user_id: int, user: User):
    return modify(user_id, user)


@app.get('/get/all/')
async def get_all():
    qry = "select * from user"
    curs.execute(qry)
    return [{k: v for k, v in zip(('user_id', 'name', 'email', 'password'), row)} for row in curs.fetchall()]
