class ProxyCheckResult(object):
    is_valid: bool = False
    is_annoymous: bool = False
    location: str = None
    orgnization: str = None
    region: str = None
    country: str = None
    city: str = None


class ProxyCheckServicesBase(object):
    """
    ProxyCheckServicesBase is the abstract class for proxy checking services (i.e. IP checking services).

    :raises NotImplementedError: The check() method must be implemented by the subclasses
    """

    def check(ip: str, port: int):
        raise NotImplementedError
