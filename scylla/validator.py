import json

import requests

from .tcpping import ping

IP_CHECKER_API = 'http://ipinfo.io'
IP_CHECKER_API_SSL = 'https://ipinfo.io'

__CURRENT_IP__ = None


def get_current_ip():
    global __CURRENT_IP__
    if __CURRENT_IP__:
        print('get _current_ip')
        return __CURRENT_IP__
    else:
        print('fetch _current_ip')
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
        r = requests.get(IP_CHECKER_API, proxies={'https': proxy_str, 'http': proxy_str}, verify=False)
        j = json.loads(r.text)

        if j['ip'] != get_current_ip():
            self._anonymous = True
        self._valid = True

    @property
    def latency(self):
        return self._latency

    @property
    def success_rate(self):
        return self._success_rate
