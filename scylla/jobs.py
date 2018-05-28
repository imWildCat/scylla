from scylla.database import ProxyIP
from scylla.validation_policy import ValidationPolicy
from scylla.validator import Validator
from .loggings import logger


def save_ip(p: ProxyIP):
    basic_query = ProxyIP.select().where(ProxyIP.ip == p.ip)
    count = basic_query.count()
    if count == 0:
        # logger.debug('Creating new ip record: ' + p.__str__())
        p.save()
    else:
        # logger.debug('Update an existing ip record: ' + p.__str__())

        existing_proxy: ProxyIP = ProxyIP.get(ProxyIP.ip == p.ip)

        existing_proxy.assign_from(p)

        existing_proxy.save()

        # logger.debug('Saved: ' + existing_proxy.__str__())


def validate_proxy_ip(p: ProxyIP):
    # logger.debug('Validating ip: {}'.format(p.ip))
    policy = ValidationPolicy(proxy_ip=p)

    if not policy.should_validate():
        return

    v = Validator(host=p.ip, port=int(p.port), using_https=policy.should_try_https())

    try:
        v.validate()
    except (KeyboardInterrupt, SystemExit):
        logger.info('KeyboardInterrupt terminates validate_proxy_ip: ' + p.ip)

    meta = v.meta if v.meta else {}
    validated_ip = ProxyIP(ip=p.ip, port=p.port, **meta)
    # save valid ip into database
    validated_ip.latency = v.latency
    validated_ip.stability = v.success_rate
    validated_ip.is_valid = v.valid
    validated_ip.is_anonymous = v.anonymous

    # Increase attempts and https_attempts
    validated_ip.attempts = validated_ip.attempts + 1
    if v.using_https:
        validated_ip.https_attempts = validated_ip.https_attempts + 1

    if v.valid:
        validated_ip.is_https = v.using_https

    # logger.debug('Save valid ip into database: \n' + validated_ip.__str__())

    save_ip(validated_ip)

    # logger.debug('Finish validating ip: {}'.format(validated_ip.ip))
