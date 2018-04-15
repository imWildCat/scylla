from requests_html import HTML

from scylla.database import ProxyIP
from scylla.providers import BaseProvider


class XiciProvider(BaseProvider):

    def urls(self) -> [str]:
        return [
            'http://www.xicidaili.com/nn',
            'http://www.xicidaili.com/wn',
        ]

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ip_row in html.find('#ip_list tr'):

            ip_element = ip_row.find('td:nth-child(2)', first=True)
            port_element = ip_row.find('td:nth-child(3)', first=True)

            if ip_element and port_element:
                p = ProxyIP(ip=ip_element.text, port=port_element.text)
                ip_list.append(p)

        return ip_list

    @staticmethod
    def should_render_js() -> bool:
        return False
