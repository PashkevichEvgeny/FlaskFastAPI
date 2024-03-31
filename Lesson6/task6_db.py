# Describing Databases with MetaData

import databases
import sqlalchemy
from sqlalchemy import String, Integer, Column, ForeignKey, Table

DATABASE_URL = "sqlite:///task6db.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


clients = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(32)),
    Column("surname", String(32)),
    Column("email", String(128)),
    Column("password", String(128)),
)


products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(32)),
    Column("description", String(256)),
    Column("price", Integer),
)


orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("client_id", Integer, ForeignKey("clients.id"), nullable=False),
    Column("product_id", Integer, ForeignKey("products.id"), nullable=False),
    Column("date_order", String(16)),
    Column("status_order", String(16)),
)
