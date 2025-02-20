import datetime
import math

from peewee import CharField, DateTimeField, BooleanField, FloatField, IntegerField, SqliteDatabase
from playhouse.signals import pre_save, Model

from scylla.config import get_config
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
        logger.debug('create new db connection')
        _db = SqliteDatabase(get_config('db_path', './scylla.db'))
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
        indexes = (
            (('ip', 'port'), True),
        )

    ip = CharField()
    port = IntegerField()
    is_valid = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    latency = FloatField()
    stability = FloatField()
    is_anonymous = BooleanField(default=False)
    is_https = BooleanField(default=False)
    attempts = IntegerField(default=0)
    https_attempts = IntegerField(default=0)
    location = CharField(null=True)
    organization = CharField(null=True)
    region = CharField(null=True)
    country = CharField(null=True)
    city = CharField(null=True)
    asn = CharField(null=True)
    isp = CharField(null=True)
    state = CharField(null=True)
    zipcode = CharField(null=True)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    timezone = CharField(null=True)
    localtime = DateTimeField(null=True)
    is_mobile = BooleanField(default=False)
    is_vpn = BooleanField(default=False)
    is_tor = BooleanField(default=False)
    is_proxy = BooleanField(default=False)
    is_datacenter = BooleanField(default=False)
    risk_score = IntegerField(null=True)

    def assign_from(self, p):
        self.ip = p.ip
        self.port = p.port
        self.is_valid = p.is_valid
        self.latency = p.latency
        self.stability = p.stability
        self.is_anonymous = p.is_anonymous
        if not self.is_https:
            # Prevent downgrading https proxy to http proxy
            self.is_https = p.is_https
        self.attempts = p.attempts
        self.https_attempts = p.https_attempts
        self.location = p.location
        self.organization = p.organization
        self.region = p.region
        self.country = p.country
        self.city = p.city
        self.asn = p.asn
        self.isp = p.isp
        self.state = p.state
        self.zipcode = p.zipcode
        self.latitude = p.latitude
        self.longitude = p.longitude
        self.timezone = p.timezone
        self.localtime = p.localtime
        self.is_mobile = p.is_mobile
        self.is_vpn = p.is_vpn
        self.is_tor = p.is_tor
        self.is_proxy = p.is_proxy
        self.is_datacenter = p.is_datacenter
        self.risk_score = p.risk_score
        self.updated_at = datetime.datetime.now()

    def __str__(self):
        return '[database.ProxyIP ip: {}, port: {}, is_valid: {}, latency: {}]' \
            .format(self.ip, self.port, self.is_valid, self.latency)

    def __repr__(self):
        return self.__str__()


@pre_save(sender=ProxyIP)
def proxy_ip_on_pre_save_handler(model_class, instance: ProxyIP, created):
    instance.latency = math.floor(instance.latency)
