from requests_html import HTML

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class IpaddressProvider(BaseProvider):

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ip_row in html.find('.proxylist tbody tr'):
            ip_port = ip_row.find('td:nth-child(1)', first=True).text
            ip_address, port = ip_port.split(":")

            p = ProxyIP(ip=ip_address, port=port)

            ip_list.append(p)

        return ip_list

    def urls(self) -> [str]:
        return [
            'https://www.ipaddress.com/proxy-list/'
        ]
