# Разработать API для управления списком пользователей с использованием базы данных SQLite.
# Для этого создайте модель User со следующими полями:
# - id:       int (идентификатор пользователя, генерируется автоматически)
# - username: str (имя пользователя)
# - email:    str (электронная почта пользователя)
# - password: str (пароль пользователя)
#
# API должно поддерживать следующие операции:
# - Получение списка всех пользователей:            GET /users/
# - Получение информации о конкретном пользователе: GET /users/{user_id}/
# - Создание нового пользователя:                   POST /users/
# - Обновление информации о пользователе:           PUT /users/{user_id}/
# - Удаление пользователя:                          DELETE /users/{user_id}/
# Для валидации данных используйте параметры Field модели User.
# Для работы с базой данных используйте SQLAlchemy и модуль databases.
from pydantic import BaseModel
import databases
import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import create_engine
from typing import List

app = FastAPI()

DATABASE_URL = "sqlite:///task1db.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


# Создание и удаление БД
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(32)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(128)),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание таблицы
metadata.create_all(engine)


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str


class UserIn(BaseModel):
    username: str
    email: str
    password: str


@app.get('/users/', response_model=List[User])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}', response_model=User)
async def get_user_by_id(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.post('/users/', response_model=User)
async def add_user(user: UserIn):
    query = users.insert().values(username=user.username, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.put('/users/{user_id}', response_model=User)
async def edit_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(count):
        query = users.insert().values(username=f'user{i}', email=f'mail{i}@gmail.com', password=f'pa%ss{i}wORD{i + 1}')
        await database.execute(query)
    return {'message': f'{count} fake users created'}
