from scylla.database import ProxyIP
from scylla.validator import Validator


def validate_proxy_ip(p: ProxyIP):
    v = Validator(host=p.ip, port=int(p.port))
    v.validate()
    # save valid ip into database
