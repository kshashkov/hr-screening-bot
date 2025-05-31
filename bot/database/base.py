from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

my_metadata = MetaData()


class Base(DeclarativeBase):
    metadata = my_metadata
