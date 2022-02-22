import peeweedbevolve
from load_all import sqlite_db
from peewee import *


class BaseModel(Model):
    class Meta:
        database = sqlite_db


if __name__ == '__main__':
    sqlite_db.evolve(interactive=False)
