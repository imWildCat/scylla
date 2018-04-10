import datetime

from peewee import Model, CharField, DateTimeField, BooleanField, FloatField, IntegerField, SqliteDatabase

_db = None


def create_connection() -> SqliteDatabase:
    global _db
    if _db:
        return _db
    else:
        print('create new connection')
        _db = SqliteDatabase('scylla.db')
        return _db


def create_db_tables():
    db = create_connection()
    db.create_tables([ProxyIP])


class BaseModel(Model):
    class Meta:
        database = create_connection()


class ProxyIP(BaseModel):
    class Meta:
        table_name = 'proxy_ips'

    ip = CharField(unique=True)
    port = IntegerField()
    is_valid = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    latency = FloatField()
    stability = FloatField()
    is_anonymous = BooleanField(default=False)
