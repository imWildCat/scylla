import re

from pyquery import PyQuery

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class PlainTextProvider(BaseProvider):

    def urls(self) -> [str]:
        return []

    def parse(self, document: PyQuery) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        if document is None:
            return []

        text = document.html()

        for ip_port in text.split('\n'):
            if ip_port.strip() == '' or not re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:(\d{2,5})', ip_port):
                continue
            ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip_port).group(0)
            port = re.search(r':(\d{2,5})', ip_port).group(1)

            if ip and port:
                p = ProxyIP(ip=ip, port=port)
                ip_list.append(p)

        return ip_list

    @staticmethod
    def should_render_js() -> bool:
        return False
