from datetime import datetime, timedelta

from scylla.database import ProxyIP


class ValidationPolicy(object):
    """
    ValidationPolicy will make decision about validating a proxy IP from the following aspects:
    1. Whether or not to validate the proxy
    2. Use http or https to validate the proxy

    After 3 attempts, the validator should try no more attempts in 24 hours after its creation.
    """
    proxy_ip: ProxyIP = None

    def __init__(self, proxy_ip: ProxyIP):
        """
        Constructor of ValidationPolicy
        :param proxy_ip: the ProxyIP instance to be validated
        """
        self.proxy_ip = proxy_ip

    def should_validate(self) -> bool:
        if self.proxy_ip.attempts == 0:
            return True
        elif self.proxy_ip.attempts < 3 \
                and datetime.now() - self.proxy_ip.created_at < timedelta(hours=24) \
                and not self.proxy_ip.is_valid:
            # If the proxy is created within 24 hours, the maximum attempt count is 3
            return True
        elif timedelta(hours=48) > datetime.now() - self.proxy_ip.created_at > timedelta(hours=24) \
                and self.proxy_ip.attempts < 6:
            # The proxy will be validated up to 6 times with in 48 hours after 24 hours
            return True
        elif datetime.now() - self.proxy_ip.created_at < timedelta(days=7) \
                and self.proxy_ip.attempts < 21 \
                and self.proxy_ip.is_valid:
            # After 48 hours the proxy is created, the proxy will be validated up to
            # 21 times (3 times a day on average) if it is valid within 7 days.
            return True
        # By default, return False
        return False

    def should_try_https(self) -> bool:
        if self.proxy_ip.is_valid and self.proxy_ip.attempts < 3 \
                and self.proxy_ip.https_attempts == 0:
            # Try https proxy for the 2nd and 3rd time if the proxy is valid
            return True

        return False
