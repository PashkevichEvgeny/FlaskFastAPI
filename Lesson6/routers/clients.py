from typing import List

from fastapi import APIRouter

from Lesson6.task6_db import clients, database
from Lesson6.task6_model import Client, ClientIn

router = APIRouter()


@router.get('/', response_model=List[Client])
async def get_clients():
    query = clients.select()
    return await database.fetch_all(query)


@router.get('/{client_id}/', response_model=Client | None)
async def get_client_by_id(client_id: int):
    query = clients.select().where(clients.c.id == client_id)
    return await database.fetch_one(query)


@router.post('/', response_model=Client)
async def add_client(client: ClientIn):
    query = clients.insert().values(name=client.name,
                                    surname=client.surname,
                                    email=client.email,
                                    password=client.password,)
    last_record_id = await database.execute(query)
    return {**client.model_dump(), "id": last_record_id}


@router.put('/{client_id}/', response_model=Client)
async def edit_client(client_id: int, new_client: ClientIn):
    query = clients.update().where(clients.c.id == client_id).values(**new_client.model_dump())
    await database.execute(query)
    return {**new_client.model_dump(), "id": client_id}


@router.delete('/{client_id}/')
async def delete_client(client_id: int):
    query = clients.delete().where(clients.c.id == client_id)
    await database.execute(query)
    return {'message': 'Client deleted'}
