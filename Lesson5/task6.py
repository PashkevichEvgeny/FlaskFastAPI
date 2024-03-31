# Создать веб-страницу для отображения списка пользователей. Приложение должно использовать
#  шаблонизатор Jinja для динамического формирования HTML страницы.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте HTML шаблон для отображения списка пользователей. Шаблон должен содержать
#  заголовок страницы, таблицу со списком пользователей и кнопку для добавления нового пользователя.
# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja.
import random
from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from Lesson5.db import curs, conn
from Lesson5.model_user import User

app = FastAPI()

templates = Jinja2Templates(directory="Lesson5/templates")


def get_all():
    qry = "select * from user"
    curs.execute(qry)
    return [{k: v for k, v in zip(('user_id', 'name', 'email', 'password'), row)} for row in curs.fetchall()]


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    users = get_all()
    return templates.TemplateResponse("all.html", {"request": request, "users": users})


def get_one(user_id: int) -> User:
    qry = "select * from user where user_id=:user_id"
    params = {"user_id": user_id}
    curs.execute(qry, params)
    id_, name, email, password = curs.fetchone()
    return User(user_id=id_, name=name, email=email, password=password)


def create(name: str, user: User) -> User:
    qry = "insert into user values (:user_id, :name, :email, :password)"
    user.name = name.lower()
    user.email = f'{name}@{name}mail.com'.lower()
    params = user.dict()
    curs.execute(qry, params)
    conn.commit()
    return user


@app.get("/login/", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse("form.html", {"request": request, 'title': 'Тест форма'})


@app.post("/login/")
async def login(name: Annotated[str, Form()], email: Annotated[EmailStr, Form()], password: Annotated[str, Form()]):
    user = User(user_id=random.randint(1, 10000000), name=name, email=email, password=password)
    create(name, user)
    return {'use': user.model_dump()}
