import re

from requests_html import HTML

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class CoolProxyProvider(BaseProvider):

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ip_row in html.find('table tr'):

            ip_element = ip_row.find('td:nth-child(1)', first=True)
            port_element = ip_row.find('td:nth-child(2)', first=True)

            if ip_element and port_element:
                p = ProxyIP(ip=re.sub(r'document\.write\(.+\)', '', ip_element.text), port=port_element.text)

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
