import json

import requests

from .loggings import logger
from .tcpping import ping

IP_CHECKER_API = 'http://ipinfo.io'
IP_CHECKER_API_SSL = 'https://ipinfo.io'

__CURRENT_IP__ = None


def get_current_ip():
    global __CURRENT_IP__
    if __CURRENT_IP__:
        logger.debug('get _current_ip')
        return __CURRENT_IP__
    else:
        logger.debug('fetch _current_ip')
        r = requests.get(IP_CHECKER_API)
        j = json.loads(r.text)
        __CURRENT_IP__ = j['ip']
        return __CURRENT_IP__


class Validator(object):
    def __init__(self, host: str, port: int, using_ssl: bool = False):
        self._host = host
        self._port = port

        self._checking_api = IP_CHECKER_API_SSL if using_ssl else IP_CHECKER_API

        # default values
        self._success_rate = 0.0
        self._latency = float('inf')

        self._anonymous = False
        self._valid = False

    def validate_latency(self):
        (self._latency, self._success_rate) = ping(self._host, self._port)

    def validate_proxy(self):
        proxy_str = 'http://{}:{}'.format(self._host, self._port)
        try:
            r = requests.get(IP_CHECKER_API, proxies={'https': proxy_str, 'http': proxy_str}, verify=False, timeout=15)
            if r.ok:
                j = json.loads(r.text)

                if j['ip'] != get_current_ip():
                    self._anonymous = True
                self._valid = True
        except requests.Timeout:
            logger.debug('Catch requests.Timeout for proxy ip: {}'.format(self._host))

    def validate(self):
        self.validate_latency()
        self.validate_proxy()

    @property
    def latency(self):
        return self._latency

    @property
    def success_rate(self):
        return self._success_rate

    @property
    def valid(self):
        return self._valid

    @property
    def anonymous(self):
        return self._anonymous
