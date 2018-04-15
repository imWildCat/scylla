import datetime

from scylla.database import ProxyIP
from scylla.validator import Validator
from .loggings import logger


def save_ip(p: ProxyIP):
    basic_query = ProxyIP.select().where(ProxyIP.ip == p.ip)
    count = basic_query.count()
    if count == 0:
        logger.debug('Creating new ip record: ' + p.__str__())
        p.save()
    else:
        logger.debug('Update an existing ip record: ' + p.__str__())

        ProxyIP.update(latency=p.latency, stability=p.stability, is_valid=p.is_valid,
                       is_anonymous=p.is_anonymous, updated_at=datetime.datetime.now()).where(
            ProxyIP.ip == p.ip).execute()

        logger.debug('Saved: ' + p.__str__())


def validate_proxy_ip(p: ProxyIP):
    logger.debug('Validating ip: {}'.format(p.ip))
    v = Validator(host=p.ip, port=int(p.port))

    try:
        v.validate()
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt terminates validate_proxy_ip: ' + p.ip)

    meta = v.meta if v.meta else {}
    validated_ip = ProxyIP(ip=p.ip, port=p.port, **meta)
    # save valid ip into database
    validated_ip.latency = v.latency
    validated_ip.stability = v.success_rate
    validated_ip.is_valid = v.valid
    validated_ip.is_anonymous = v.anonymous

    logger.debug('Save valid ip into database: \n' + validated_ip.__str__())

    save_ip(validated_ip)

    logger.debug('Finish validating ip: {}'.format(validated_ip.ip))
