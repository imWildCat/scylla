from scylla.database import ProxyIP


class ValidationTask(object):
    """
    Class ValidationTask is the representation of the task for validating a proxy IP.
    The validator_queue will deque instances of this class, trying to validate the proxy contained.
    The maximum number of validation attempts is 6.
    As for attempt #0, #2, #4, the validator will try HTTP proxy.
    As for attempt #1, #3, #5, the validator will try HTTPS proxy.
    After 6 attempts, the validator should try no more attempts.
    """
    proxy_ip: ProxyIP = None
    num_of_attempts: int = 0

    def __init__(self, proxy_ip: ProxyIP):
        """
        Constructor of ValidationTask
        :param proxy_ip: the ProxyIP instance to be validated
        """
        self.proxy_ip = proxy_ip

    def increase_num_of_attempts(self):
        self.num_of_attempts += 1
