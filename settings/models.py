from .config import sqlite_db
from peewee import *


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class UserToken(BaseModel):
    user = IntegerField()
    chat = IntegerField()
    token = CharField(max_length=255, null=True, default=None)
    is_login = BooleanField(default=False)


if __name__ == '__main__':
    sqlite_db.connect()
    UserToken.create_table()
    UserToken.update()
