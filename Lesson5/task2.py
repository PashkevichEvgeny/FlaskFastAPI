# Создать API для получения списка фильмов по жанру.
# Приложение должно иметь возможность получать список фильмов по заданному жанру.
# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс Movie с полями id, title, description и genre.
# Создайте список movies для хранения фильмов.
# Создайте маршрут для получения списка фильмов по жанру (метод GET).
# Реализуйте валидацию данных запроса и ответа.
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Movie(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genre: str


class GenreName(str, Enum):
    Action = 'Action'
    Drama = 'Drama'
    Comedy = 'Comedy'
    Detective = 'Detective'


movies: list = []
genre: list = ['Action', 'Drama', 'Comedy', 'Detective']


@app.get('/genre/{genre}/')
async def get_movies_by_genre(genre: GenreName):
    temp = []
    for movie in movies:
        if movie.genre == genre:
            temp.append(movie)
    if temp:
        return {genre: temp}
    return 'Not found'


@app.post('/add-movies/')
async def add_movies(amount: int = 16):
    make_movies(amount)
    return {'Movies added': movies}


@app.get('/')
async def get():
    return {'Movies in database': movies}


def make_movies(amount):
    list_genre = [g.value for g in GenreName]
    for i in range(amount):
        n = i + 1
        movies.append(Movie(id=n, title=f'Name{n}', description=f'Description movie-{n}', genre=list_genre[i % 4]))
