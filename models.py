import peeweedbevolve
from load_all import sqlite_db
from peewee import *


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class UserToken(BaseModel):
    user = IntegerField()
    chat = IntegerField()
    token = CharField(max_length=255, default=None)


if __name__ == '__main__':
    sqlite_db.connect()
    UserToken.create_table()
    UserToken.update()
