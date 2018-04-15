from scylla.database import ProxyIP
from scylla.validator import Validator
from .loggings import logger


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
    logger.debug('Validating ip: {}'.format(p.ip))
    v = Validator(host=p.ip, port=int(p.port))
    v.validate()
    # save valid ip into database
    p.latency = v.latency
    p.stability = v.success_rate
    p.is_valid = v.valid
    p.is_anonymous = v.anonymous

    logger.debug('Save valid ip into database: \n' + p.__str__())

    save_ip(p)

    logger.debug('Finish validating ip: {}'.format(p.ip))
