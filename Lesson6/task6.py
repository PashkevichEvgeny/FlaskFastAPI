# Необходимо создать базу данных для интернет-магазина.
# База данных должна состоять из трех таблиц: товары, заказы и пользователи.
# Таблица товары должна содержать информацию о доступных товарах, их описаниях и ценах.
# Таблица пользователи должна содержать информацию о зарегистрированных пользователях магазина.
# Таблица заказы должна содержать информацию о заказах, сделанных пользователями.
# - Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
#                                                          имя,
#                                                          фамилия,
#                                                          адрес электронной почты и
#                                                          пароль.
# - Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
#                                                    название,
#                                                    описание и
#                                                    цена.
# - Таблица заказов должна содержать следующие поля: id (PRIMARY KEY),
#                                                    id пользователя (FOREIGN KEY),
#                                                    id товара (FOREIGN KEY),
#                                                    дата заказа и
#                                                    статус заказа.
# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из 3 таблиц (6 моделей).
# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API (итого 15 маршрутов).
# - Чтение всех, Чтение одного, Запись, Изменение, Удаление
from fastapi import FastAPI
from sqlalchemy import create_engine

from Lesson6.routers.clients import router as router_client
from Lesson6.routers.products import router as router_product
from Lesson6.routers.orders import router as router_order
from Lesson6.task6_db import metadata, DATABASE_URL, database

app = FastAPI()


# Создание и удаление БД
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание таблицы
metadata.create_all(engine)

app.include_router(router_client, prefix='/clients', tags=['Clients'])
app.include_router(router_product, prefix='/products', tags=['Products'])
app.include_router(router_order, prefix='/orders', tags=['Orders'])
