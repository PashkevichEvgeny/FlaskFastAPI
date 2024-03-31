from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class StatusOrder(str, Enum):
    IsPlaced = 'Is placed'
    InProgress = 'In progress'
    Completed = 'Completed'


class Client(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    password: str


class ClientIn(BaseModel):
    name: str = Field(min_length=2)
    surname: str = Field(min_length=6)
    email: EmailStr
    password: str = Field(min_length=6)


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: int


class ProductIn(BaseModel):
    name: str = Field(min_length=2)
    description: str = Field(min_length=6)
    price: int = Field(gt=0)


class Order(BaseModel):
    id: int
    client_id: int
    product_id: int
    date_order: str
    status_order: StatusOrder


class OrderIn(BaseModel):
    client_id: int
    product_id: int
    date_order: str = datetime.now().strftime('%Y-%m-%d')
    status_order: StatusOrder = StatusOrder.IsPlaced


