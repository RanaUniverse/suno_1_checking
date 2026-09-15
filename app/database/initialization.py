"""
app/database/initialization.py

This will create the database tables and so on
so here first i will import all the tables first

i need to call this fun at startup later i will use alembic

I will not use this rather i will use Alembic not this
"""

from sqlmodel import SQLModel


from .engine import engine

# This models module is where all the class of table will be defined
from .models import *


def create_db_and_tables():
    print("Database Table is Making Now...")
    SQLModel.metadata.create_all(
        bind=engine,
    )
    print("Database Table Has Been Created!!!")
