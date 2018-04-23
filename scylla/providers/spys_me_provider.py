import re

from requests_html import HTML

from scylla.database import ProxyIP
from scylla.providers import BaseProvider


class SpyMeProvider(BaseProvider):

    def urls(self) -> [str]:
        return [
            'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt',
        ]

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        text = html.raw_html

        ip_port_str_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5}', text.decode('utf-8'))

        for ip_port in ip_port_str_list:

            ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip_port).group(0)
            port = re.search(r':(\d{2,5})', ip_port).group(1)

            if ip and port:
                p = ProxyIP(ip=ip, port=port)
                ip_list.append(p)

        return ip_list

    @staticmethod
    def should_render_js() -> bool:
        return False
