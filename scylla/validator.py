import json
import math
import time

import requests

from .loggings import logger
from .tcpping import ping
from .worker import DEFAULT_USER_AGENT, DEFAULT_TIMEOUT_SECONDS

IP_CHECKER_API = 'http://api.ipify.org/?format=json'
IP_CHECKER_API_SSL = 'https://api.ipify.org/?format=json'

__CURRENT_IP__ = None


def get_current_ip():
    global __CURRENT_IP__
    if __CURRENT_IP__:
        # logger.debug('get_current_ip from cache')
        return __CURRENT_IP__
    else:
        # logger.debug('fetch current_ip')
        r = requests.get(IP_CHECKER_API)
        j = json.loads(r.text)
        __CURRENT_IP__ = j['ip']
        return __CURRENT_IP__


class Validator(object):
    def __init__(self, host: str, port: int, using_https: bool = False):
        self._host = host
        self._port = port

        self._using_https = using_https

        # default values
        self._success_rate = 0.0
        self._latency = float('inf')

        self._anonymous = False
        self._valid = False

        self._meta = None

    def validate_latency(self):
        try:
            (self._latency, self._success_rate) = ping(self._host, self._port)
        except ConnectionRefusedError:
            self._latency, self._success_rate = math.inf, 0.0

    def validate_proxy(self):
        protocol = 'https' if self._using_https else 'http'
        proxy_str = '{}://{}:{}'.format(protocol, self._host, self._port)
        time.sleep(3)
        try:
            checking_api = IP_CHECKER_API_SSL if self._using_https else IP_CHECKER_API

            # First request for checking IP
            r = requests.get(checking_api, headers={'user-agent': DEFAULT_USER_AGENT},
                             proxies={'https': proxy_str, 'http': proxy_str}, verify=False,
                             timeout=DEFAULT_TIMEOUT_SECONDS)
            if r.ok:
                j = json.loads(r.text)

                if j['ip'] != get_current_ip():
                    self._anonymous = True
                self._valid = True

                # A second request for meta info
                r2 = requests.get('https://api.ip.sb/geoip/{}'.format(j['ip']),
                                  headers={'user-agent': DEFAULT_USER_AGENT}, verify=False,
                                  timeout=DEFAULT_TIMEOUT_SECONDS)
                jresponse = r2.json()

                # Load meta data
                # TODO: better location check
                meta = {
                    'location': '{},{}'.format(jresponse['latitude'], jresponse['longitude']),
                    'organization': jresponse['organization'] if 'organization' in jresponse else None,
                    'region': jresponse['region'],
                    'country': jresponse['country_code'],
                    'city': jresponse['city'],
                }
                self._meta = meta

        except requests.Timeout:
            logger.debug('Catch requests.Timeout for proxy ip: {}'.format(self._host))
        except requests.RequestException as e:
            logger.debug('Catch requests.RequestException for proxy ip: {}'.format(self._host))
            logger.debug(e.__str__())

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

    @property
    def meta(self):
        return self._meta

    @property
    def using_https(self):
        return self._using_https
