from requests_html import HTML

from scylla.providers import BaseProvider
from scylla.proxy_ip import ProxyIP


class KuaidailiProvider(BaseProvider):

    def urls(self) -> [str]:
        return [
            'https://www.kuaidaili.com/free/inha/1/',
        ]

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ip_row in html.find('#list table tr'):

            ip_element = ip_row.find('td[data-title="IP"]', first=True)
            port_element = ip_row.find('td[data-title="PORT"]', first=True)

            if ip_element and port_element:
                p = ProxyIP(ip_element.text, port_element.text)
                ip_list.append(p)

        return ip_list

    @staticmethod
    def should_render_js() -> bool:
        return False
