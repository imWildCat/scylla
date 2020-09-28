import requests


class BaseValidator(object):

    check_url = 'https://www.google.com'

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

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

