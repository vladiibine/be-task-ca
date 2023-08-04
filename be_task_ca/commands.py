from .database import engine, Base

# just importing all the models is enough to have them created
# flake8: noqa
from .user import sa_postgres_model
from .item import sa_postgres_model


def create_db_schema():
    Base.metadata.create_all(bind=engine)
