import json

from pyquery import PyQuery

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class ProxyScraperProvider(BaseProvider):

    def urls(self) -> [str]:
        return ['https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list']

    def parse(self, document: PyQuery) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for i in document.text.split("\n"):
            if len(i) > 0:
                jo = json.loads(i)
                p = ProxyIP(ip=jo['host'], port=jo['port'])
                ip_list.append(p)
        return ip_list

    @staticmethod
    def should_render_js() -> bool:
        return False
