import datetime

from peewee import Model, CharField, DateTimeField, BooleanField, FloatField, IntegerField, SqliteDatabase

from scylla.loggings import logger

_db = None


def create_connection() -> SqliteDatabase:
    """
    create a database connection
    :rtype: SqliteDatabase
    """
    global _db
    if _db:
        return _db
    else:
        logger.debug('create new connection')
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
    is_valid = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    latency = FloatField()
    stability = FloatField()
    is_anonymous = BooleanField(default=False)
    location = CharField(null=True)
    organization = CharField(null=True)
    region = CharField(null=True)
    country = CharField(null=True)
    city = CharField(null=True)

    def __str__(self):
        return '[database.ProxyIP ip: {}, port: {}, is_valid: {}, latency: {}]' \
            .format(self.ip, self.port, self.is_valid, self.latency)

    def __repr__(self):
        return self.__str__()
