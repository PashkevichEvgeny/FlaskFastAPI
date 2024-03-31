from typing import List

from fastapi import APIRouter

from Lesson6.task6_db import products, database
from Lesson6.task6_model import Product, ProductIn

router = APIRouter()


@router.get('/', response_model=List[Product])
async def get_products():
    query = products.select()
    return await database.fetch_all(query)


@router.get('/{product_id}/', response_model=Product | None)
async def get_product_by_id(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@router.post('/', response_model=Product)
async def add_product(product: ProductIn):
    query = products.insert().values(name=product.name,
                                     description=product.description,
                                     price=product.price,)
    last_record_id = await database.execute(query)
    return {**product.model_dump(), "id": last_record_id}


@router.put('/{product_id}/', response_model=Product)
async def edit_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), "id": product_id}


@router.delete('/{product_id}/')
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'Product deleted'}
