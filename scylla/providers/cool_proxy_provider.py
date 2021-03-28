import re

from pyquery import PyQuery

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class CoolProxyProvider(BaseProvider):

    def parse(self, document: PyQuery) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ip_row in document.find('table tr'):
            ip_row: PyQuery = ip_row
            ip_element: PyQuery = ip_row.find('td:nth-child(1)')
            port_element: PyQuery = ip_row.find('td:nth-child(2)')

            if ip_element and port_element:
                p = ProxyIP(ip=re.sub(r'document\.write\(.+\)', '', ip_element.text()), port=port_element.text())

                ip_list.append(p)

        return ip_list

    def urls(self) -> [str]:
        return [
            'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:1',
            'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:1/page:2',
            'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:1/page:3',
        ]

    @staticmethod
    def should_render_js() -> bool:
        return True
