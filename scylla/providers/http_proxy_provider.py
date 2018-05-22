from requests_html import HTML

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class HttpProxyProvider(BaseProvider):

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ip_row in html.find('table.proxytbl tr'):

            ip_element = ip_row.find('td:nth-child(1)', first=True)
            port_element = ip_row.find('td:nth-child(2)', first=True)

            if ip_element and port_element:
                p = ProxyIP(ip=ip_element.text, port=port_element.text)

                ip_list.append(p)

        return ip_list

    def urls(self) -> [str]:
        return [
            'https://proxyhttp.net/free-list/proxy-anonymous-hide-ip-address/',
            'https://proxyhttp.net/',
            'https://proxyhttp.net/free-list/anonymous-server-hide-ip-address/2#proxylist',
        ]

    @staticmethod
    def should_render_js() -> bool:
        return False
