# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание.
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
# API должен содержать следующие конечные точки:
#  - GET /tasks - возвращает список всех задач.
#  - GET /tasks/{id} - возвращает задачу с указанным идентификатором.
#  - POST /tasks - добавляет новую задачу.
#  - PUT /tasks/{id} - обновляет задачу с указанным идентификатором.
#  - DELETE /tasks/{id} - удаляет задачу с указанным идентификатором.
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class TaskStatus(str, Enum):
    in_progress = 'in progress'
    done = 'done'


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus = TaskStatus.in_progress


tasks = list()


@app.get('/tasks')
async def get_tasks() -> List[Task]:
    return [task for task in tasks]


@app.get('/tasks/{task_id}')
async def get_tasks(task_id: int = 0) -> Task | None:
    for task in tasks:
        if task.id == task_id:
            return task
    return None


@app.post('/tasks')
async def create_task(task: Task) -> Task | None:
    if task not in tasks:
        tasks.append(task)
        return task
    return None


@app.put('/tasks/{task_id}')
async def update_task(status: TaskStatus, task_id: int = 0) -> Task | None:
    for task in tasks:
        if task.id == task_id:
            task.status = status
        return task
    return None


@app.delete('/tasks/{task_id}')
async def delete_task(task_id: int = 0) -> Task | None:
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return task
    return None



