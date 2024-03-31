# Напишите API для управления списком задач. Для этого создайте модель Task со следующими полями:
# - id:          int (первичный ключ)
# - title:       str (название задачи)
# - description: str (описание задачи)
# - done:        bool (статус выполнения задачи)
#
# API должно поддерживать следующие операции:
# - Получение списка всех задач:              GET /tasks/
# - Получение информации о конкретной задаче: GET /tasks/{task_id}/
# - Создание новой задачи:                    POST /tasks/
# - Обновление информации о задаче:           PUT /tasks/{task_id}/
# - Удаление задачи:                          DELETE /tasks/{task_id}/
# Для валидации данных используйте параметры Field модели Task.
# Для работы с базой данных используйте SQLAlchemy и модуль databases.
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import create_engine
from typing import List


class Task(BaseModel):
    id: int
    title: str = Field(min_length=2)
    description: str | None = None
    status: bool = False


class TaskIn(BaseModel):
    title: str = Field(min_length=2)
    description: str | None = None
    status: bool = False


app = FastAPI()


DATABASE_URL = "sqlite:///task4db.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


# Создание и удаление БД
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
    sqlalchemy.Column("status", sqlalchemy.Boolean),
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание таблицы
metadata.create_all(engine)


@app.get('/tasks/', response_model=List[Task])
async def get_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.get('/tasks/{task_id}', response_model=Task)
async def get_task_by_id(task_id: int):
    query = tasks.select().where(tasks.c.id == task_id)
    return await database.fetch_one(query)


@app.post('/tasks/', response_model=Task)
async def add_task(task: TaskIn):
    query = tasks.insert().values(title=task.title, description=task.description, status=task.status,)
    last_record_id = await database.execute(query)
    return {**task.model_dump(), "id": last_record_id}


@app.put('/tasks/{task_id}', response_model=Task)
async def edit_task(task_id: int):
    query = tasks.update().where(tasks.c.id == task_id).values(status=True,)
    await database.execute(query)
    query = tasks.select().where(tasks.c.id == task_id)
    task = await database.fetch_one(query)
    return {**task, "id": task_id}


@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {'message': 'Task deleted'}
