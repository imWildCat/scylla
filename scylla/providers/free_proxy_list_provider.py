from pyquery import PyQuery

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class FreeProxyListProvider(BaseProvider):

    def parse(self, document: PyQuery) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ip_row in document.find('#proxylisttable tbody tr'):
            ip_row: PyQuery = PyQuery(ip_row)
            ip_address: str = ip_row.find('td:nth-child(1)').text()
            port: str = ip_row.find('td:nth-child(2)').text()

            p = ProxyIP(ip=ip_address, port=port)

            ip_list.append(p)

        return ip_list

    def urls(self) -> [str]:
        return [
            'https://free-proxy-list.net/'
        ]
