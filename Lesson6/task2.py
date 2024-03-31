# Создать веб-приложение на FastAPI, которое будет предоставлять API для работы с базой данных пользователей.
# Пользователь должен иметь следующие поля:
# - ID (автоматически генерируется при создании пользователя)
# - Имя (строка, не менее 2 символов)
# - Фамилия (строка, не менее 2 символов)
# - Дата рождения (строка в формате "YYYY-MM-DD")
# - Email (строка, валидный email)
# - Адрес (строка, не менее 5 символов)
#
# API должен поддерживать следующие операции:
# - Добавление пользователя в базу данных
# - Получение списка всех пользователей в базе данных
# - Получение пользователя по ID
# - Обновление пользователя по ID
# - Удаление пользователя по ID
# Приложение должно использовать базу данных SQLite3 для хранения пользователей.
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
import databases
import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import create_engine
from typing import List


class User(BaseModel):
    id: int
    name: str = Field(title='Name', min_length=2)
    surname: str = Field(title='Surname', min_length=2)
    birthday: str = Field(title='Birthday')
    email: EmailStr = Field(title='Email')
    address: str = Field(title='Address', min_length=5)

    @field_validator('birthday')
    def parse_datetime(cls, value: str):
        if datetime.strptime(value, '%Y-%m-%d'):
            return value
        return 'Wrong date format'


class UserIn(BaseModel):
    id: int
    name: str = Field(title='Name', min_length=2)
    surname: str = Field(title='Surname', min_length=2)
    birthday: str = Field(title='Birthday')
    email: EmailStr = Field(title='Email')
    address: str = Field(title='Address', min_length=5)

    @field_validator('birthday')
    def parse_datetime(cls, value: str):
        if datetime.strptime(value, '%Y-%m-%d'):
            return value
        return 'Wrong date format'


app = FastAPI()


DATABASE_URL = "sqlite:///task2db.db"
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
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(32)),
    sqlalchemy.Column("birthday", sqlalchemy.String(11)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("address", sqlalchemy.String(128)),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание таблицы
metadata.create_all(engine)


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
    query = users.insert().values(name=user.name,
                                  surname=user.surname,
                                  birthday=user.birthday,
                                  email=user.email,
                                  address=user.address)
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
        query = users.insert().values(name=f'user{i}',
                                      surname=f'userov{i}',
                                      birthday='1970-1-1',
                                      email=f'mail{i}@gmail.com',
                                      address=f'city{i}, street{i}, building {i}',)
        await database.execute(query)
    return {'message': f'{count} fake users created'}
