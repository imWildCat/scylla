import json
import math

import requests

from .loggings import logger
from .tcpping import ping
from .config import get_config, GeoIPAPI

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
        try:
            checking_api = IP_CHECKER_API_SSL if self._using_https else IP_CHECKER_API

            # First request for checking IP
            r = requests.get(checking_api, proxies={'https': proxy_str, 'http': proxy_str}, verify=False, timeout=15)
            if r.ok:
                j = json.loads(r.text)

                if j['ip'] != get_current_ip():
                    self._anonymous = True
                self._valid = True

                geoip_api = get_config('geoip_api', GeoIPAPI.IPSB)

                if geoip_api == GeoIPAPI.IPSB:
                    geoip_url = 'https://api.ip.sb/geoip/{}'.format(j['ip'])
                else:
                    geoip_url = 'https://api.ipquery.io/?format=json&ip={}'.format(j['ip'])

                # A second request for meta info
                r2 = requests.get(geoip_url, timeout=15)
                jresponse = r2.json()

                if geoip_api == GeoIPAPI.IPSB:
                    meta = {
                        'asn': jresponse['asn'],
                        'isp': jresponse['isp'],
                        'state': jresponse['region'],
                        'zipcode': None,
                        'latitude': jresponse['latitude'],
                        'longitude': jresponse['longitude'],
                        'timezone': jresponse['timezone'],
                        'localtime': None,
                        'is_mobile': None,
                        'is_vpn': None,
                        'is_tor': None,
                        'is_proxy': None,
                        'is_datacenter': None,
                        'risk_score': None,
                        'location': '{},{}'.format(jresponse['latitude'], jresponse['longitude']),
                        'organization': jresponse['organization'],
                        'region': jresponse['region'],
                        'country': jresponse['country_code'],
                        'city': jresponse['city'],
                    }
                else:
                    meta = {
                        'asn': jresponse['isp']['asn'],
                        'isp': jresponse['isp']['isp'],
                        'state': jresponse['location']['state'],
                        'zipcode': jresponse['location']['zipcode'],
                        'latitude': jresponse['location']['latitude'],
                        'longitude': jresponse['location']['longitude'],
                        'timezone': jresponse['location']['timezone'],
                        'localtime': jresponse['location']['localtime'],
                        'is_mobile': jresponse['risk']['is_mobile'],
                        'is_vpn': jresponse['risk']['is_vpn'],
                        'is_tor': jresponse['risk']['is_tor'],
                        'is_proxy': jresponse['risk']['is_proxy'],
                        'is_datacenter': jresponse['risk']['is_datacenter'],
                        'risk_score': jresponse['risk']['risk_score'],
                        'location': '{},{}'.format(jresponse['location']['latitude'], jresponse['location']['longitude']),
                        'organization': jresponse['isp']['org'],
                        'region': jresponse['location']['state'],
                        'country': jresponse['location']['country_code'],
                        'city': jresponse['location']['city'],
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
