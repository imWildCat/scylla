from requests_html import HTML

from scylla.database import ProxyIP
from scylla.providers import BaseProvider


class Data5uProvider(BaseProvider):

    def urls(self) -> [str]:
        return [
            'http://www.data5u.com/free/gwgn/index.shtml',
            'http://www.data5u.com/free/gngn/index.shtml',
        ]

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ip_row in html.find('.wlist > ul > li:nth-child(2) .l2'):

            ip_element = ip_row.find('span:nth-child(1)', first=True)
            port_element = ip_row.find('span:nth-child(2)', first=True)

            if ip_element and port_element:
                p = ProxyIP(ip=ip_element.text, port=port_element.text)
                ip_list.append(p)

        return ip_list

    @staticmethod
    def should_render_js() -> bool:
        return False
