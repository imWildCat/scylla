from bs4 import BeautifulSoup

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class FreeProxyListProvider(BaseProvider):

    def parse(self, document: BeautifulSoup) -> [ProxyIP]:
        ip_list: [ProxyIP] = []
        for ip_row in document('.fpl-list tbody tr').items():
            ip_address: str = ip_row.find('td:nth-child(1)').text()
            port: str = ip_row.find('td:nth-child(2)').text()

            p = ProxyIP(ip=ip_address, port=port)

            ip_list.append(p)

        return ip_list

    def urls(self) -> [str]:
        return [
            'http://sslproxies.org/',
            'http://free-proxy-list.net/',
            'https://free-proxy-list.net/anonymous-proxy.html',
            'https://www.us-proxy.org',
            'https://free-proxy-list.net/uk-proxy.html'
        ]
