from enum import Enum
from typing import List

from fastapi import APIRouter

from Lesson6.task6_db import orders, database
from Lesson6.task6_model import OrderIn, Order, StatusOrder

router = APIRouter()


@router.get('/', response_model=List[Order])
async def get_orders():
    query = orders.select()
    return await database.fetch_all(query)


@router.get('/{order_id}/', response_model=Order | None)
async def get_order_by_id(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@router.post('/', response_model=Order)
async def add_order(order: OrderIn,
                    client_id: int,
                    product_id: int,):
    order.client_id = client_id
    order.product_id = product_id
    query = orders.insert().values(**order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@router.put('/{order_id}/', response_model=Order)
async def edit_order(order_id: int,
                     new_order: OrderIn,
                     client_id: int = 0,
                     product_id: int = 0,
                     status_order: StatusOrder = StatusOrder.InProgress,):
    query = orders.select().where(orders.c.id == order_id)
    old = await database.fetch_one(query)
    new_order.client_id = client_id if client_id else old.client_id
    new_order.product_id = product_id if product_id else old.product_id
    new_order.date_order = old.date_order
    new_order.status_order = status_order if status_order else old.status_order
    query = orders.update().where(orders.c.id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@router.delete('/{order_id}/')
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
