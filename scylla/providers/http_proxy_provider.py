import re

from pyquery import PyQuery

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class HttpProxyProvider(BaseProvider):

    def parse(self, document: PyQuery) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ip_row in document.find('table.proxytbl tr'):
            ip_row: PyQuery = ip_row
            ip_element = ip_row.find('td:nth-child(1)')
            port_element = ip_row.find('td:nth-child(2)')

            try:
                if ip_element and port_element:
                    port_str = re.search(r'//]]> (\d+)', port_element.text()).group(1)

                    p = ProxyIP(ip=ip_element.text(), port=port_str)

                    ip_list.append(p)
            except AttributeError:
                pass

        return ip_list

    def urls(self) -> [str]:
        return [
            'https://proxyhttp.net/free-list/proxy-anonymous-hide-ip-address/',
            'https://proxyhttp.net/',
            'https://proxyhttp.net/free-list/anonymous-server-hide-ip-address/2#proxylist',
        ]

    @staticmethod
    def should_render_js() -> bool:
        return True
