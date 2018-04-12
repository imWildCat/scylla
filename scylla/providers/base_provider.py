from requests_html import HTML

from ..database import ProxyIP


class BaseProvider(object):
    """BaseProvider is the abstract class for the proxy providers

    :raises NotImplementedError: [if urls() or parse() is not implemented]
    """

    _sleep = 0

    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def sleep_seconds(self) -> int:
        """Return a sleep time for each request, by default it is 0

        :return: sleep time in seconds
        """
        return self._sleep

    def urls(self) -> [str]:
        """Return a list of url strings for crawling

        :return: [a list of url strings]
        :rtype: [str]
        """

        raise NotImplementedError

    def parse(self, html: HTML) -> [ProxyIP]:
        """Parse the document in order to get a list of proxies

        :param html: the HTML object from requests-html
        :return: a list of proxy ips
        """

        raise NotImplementedError

    @staticmethod
    def should_render_js() -> bool:
        """Whether needs js rendering
        By default, it is False.

        :return: a boolean value indicating whether or not js rendering is needed
        :rtype: bool
        """

        return False
