from scylla.database import ProxyIP
from scylla.validator import Validator


def save_ip(p: ProxyIP):
    basic_query = ProxyIP.select().where(ProxyIP.ip == p.ip)
    count = basic_query.count()
    if count == 0:
        p.save()
    else:
        p_id = ProxyIP.select().get().id
        p.id = p_id
        p.save()


def validate_proxy_ip(p: ProxyIP):
    v = Validator(host=p.ip, port=int(p.port))
    v.validate()
    # save valid ip into database
    save_ip(p)
