from requests_html import HTML

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class FreeProxyListProvider(BaseProvider):

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ip_row in html.find('#proxylisttable tbody tr'):
            ip_address = ip_row.find('td:nth-child(1)', first=True).text
            port = ip_row.find('td:nth-child(2)', first=True).text

            p = ProxyIP(ip=ip_address, port=port)

            ip_list.append(p)

        return ip_list

    def urls(self) -> [str]:
        return [
            'https://free-proxy-list.net/'
        ]
