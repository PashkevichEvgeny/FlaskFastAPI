# Создать API для управления списком задач.
# Приложение должно иметь возможность создавать, обновлять, удалять и получать список задач.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс Task с полями id, title, description, status.
# Создайте список tasks для хранения задач.
# Создайте маршруты для получения списка задач (метод GET),
#                   для создания новой задачи (метод POST),
#                   для обновления задачи (метод PUT),
#                   для удаления задачи (метод DELETE).
# Реализуйте валидацию данных запроса и ответа.

# для работы устанавливаем пакеты
# pip install fastapi
# pip install "uvicorn[standard]"
# запуск сервера с приложением: uvicorn main:app --reload
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: bool = False


list_tasks: list = []


@app.get("/task/all/")
async def get_all_tasks():
    if len(list_tasks):
        return {'tasks': list_tasks}
    return {'answer': 'No Tasks. Please, add tasks.'}


@app.get("/task/{task_id}")
async def get_some_task(task_id: int):
    for task in list_tasks:
        if task.id == task_id:
            return {task_id: task}
    return {task_id: 'Not found'}


@app.post("/task/add/{task_id}")
async def create_task(task_id: int, task: Task):
    if find_task(task_id):
        return {task_id: 'Task already exists'}
    task.id = task_id
    list_tasks.append(task)
    return {task_id: task}


@app.put("/task/edit/{task_id}")
async def update_task(task_id: int, status_: bool = True):
    if task := find_task(task_id):
        task.status_ = status_
        return {task_id: task}
    return {task_id: 'Not Found'}


@app.delete("/task/delete/{task_id}")
async def delete_task(task_id: int):
    if task := find_task(task_id):
        list_tasks.remove(task)
        return {task_id: 'The Task Is Deleted'}
    return {task_id: 'Not Found'}


def find_task(task_id):
    for task in list_tasks:
        if task.id == task_id:
            return task
    return False
