# Создать RESTful API для управления списком задач.
# Приложение должно использовать FastAPI и поддерживать следующие функции:
#  - Получение списка всех задач.
#  - Получение информации о задаче по её ID.
#  - Добавление новой задачи.
#  - Обновление информации о задаче по её ID.
#  - Удаление задачи по её ID.
# Каждая задача должна содержать следующие поля:
# ID (целое число), Название (строка), Описание (строка), Статус (строка): "todo", "in progress", "done".

# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс Task с полями id, title, description и status.
# Создайте список tasks для хранения задач.
# Создайте функцию get_tasks для получения списка всех задач (метод GET).
# Создайте функцию get_task для получения информации о задаче по её ID (метод GET).
# Создайте функцию create_task для добавления новой задачи (метод POST).
# Создайте функцию update_task для обновления информации о задаче по её ID (метод PUT).
# Создайте функцию delete_task для удаления задачи по её ID (метод DELETE).
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


class TaskStatus(str, Enum):
    todo = 'todo'
    in_progress = 'in progress'
    done = 'done'


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo


tasks = list()


@app.get('/task/all')
async def get_tasks() -> List[Task]:
    return [task for task in tasks]


@app.get('/task/{task_id}')
async def get_tasks(task_id: int = 0) -> Task | None:
    for task in tasks:
        if task.id == task_id:
            return task
    return None


@app.post('/create/')
async def create_task(task: Task) -> Task | None:
    if task not in tasks:
        tasks.append(task)
        return task
    return None


@app.put('/edit/{task_id}')
async def update_task(task_id: int, status: TaskStatus) -> Task | None:
    for task in tasks:
        if task.id == task_id:
            task.status = status
        return task
    return None


@app.delete('/delete/{task_id}')
async def delete_task(task_id: int) -> Task | None:
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return task
    return None
