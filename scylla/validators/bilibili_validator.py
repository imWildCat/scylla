import requests
from .base_validator import BaseValidator
from ..loggings import logger


class BilibiliValidator(BaseValidator):

    check_url: str = 'https://api.bilibili.com/'

    def validate(self, proxy_str):
        try:
            r = requests.get(self.check_url, proxies={'https': proxy_str, 'http': proxy_str}, verify=False, timeout=15)
            if not r.ok:
                logger.debug('Catch {} for proxy ip: {} when connecting to {}'.format(r.status_code, proxy_str.split(':')[0], self.check_url))
                return False
            return True
        except requests.Timeout:
            logger.debug('Catch requests.Timeout for proxy ip: {} when connecting to {}'.format(proxy_str.split(':')[0], self.check_url))
            return False
        except requests.RequestException as e:
            logger.debug('Catch requests.RequestException for proxy ip: {} when connecting to {}'.format(proxy_str.split(':')[0], self.check_url))
            logger.debug(e.__str__())
            return False
