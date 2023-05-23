from typing import List
from pyquery import PyQuery

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class IpaddressProvider(BaseProvider):

    def parse(self, document: PyQuery) -> List[ProxyIP]:
        ip_list: List[ProxyIP] = []

        for ip_row in document.find('.proxylist tbody tr'):
            ip_row: PyQuery = PyQuery(ip_row)
            ip_port: str = ip_row.find('td:nth-child(1)').text()
            ip_address, port = ip_port.split(":")

            p = ProxyIP(ip=ip_address, port=port)

            ip_list.append(p)

        return ip_list

    def urls(self) -> List[str]:
        return [
            'https://www.ipaddress.com/proxy-list/'
        ]
