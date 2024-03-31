# Создать API для удаления информации о пользователе из базы данных.
# Приложение должно иметь возможность принимать DELETE запросы и удалять информацию о пользователе из базы данных.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для удаления информации о пользователе (метод DELETE).
# Реализуйте проверку наличия пользователя в списке и удаление его из списка.
from fastapi import FastAPI

from Lesson5.db import curs, conn
from Lesson5.model_user import User

app = FastAPI()


def get_one(user_id: int) -> User:
    qry = "select * from user where user_id=:user_id"
    params = {"user_id": user_id}
    curs.execute(qry, params)
    id_, name, email, password = curs.fetchone()
    return User(user_id=id_, name=name, email=email, password=password)


def delete(user: User):
    if get_one(user.user_id):
        qry = "delete from user where user_id=:user_id"
        params = {'user_id': user.user_id}
        curs.execute(qry, params)
        conn.commit()
        return user
    return False


@app.delete('/user/delete/')
async def delete(user: User):
    return delete(user)


@app.get('/get/all/')
async def get_all():
    qry = "select * from user"
    curs.execute(qry)
    return [row.model_dump() for row in curs.fetchall()]