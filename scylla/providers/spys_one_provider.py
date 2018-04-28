import re

from requests_html import HTML

from scylla.database import ProxyIP
from scylla.providers import BaseProvider


class SpysOneProvider(BaseProvider):

    def urls(self) -> [str]:
        return [
            'http://spys.one/en/anonymous-proxy-list/',
            # 'http://spys.one/en/http-proxy-list/',
            # 'http://spys.one/en/https-ssl-proxy/',
        ]

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        print('html:', html.raw_html)

        for ip_row in html.find('table tr[onmouseover]'):

            ip_port_text_elem = ip_row.find('.spy14', first=True)

            if ip_port_text_elem:
                ip_port_text = ip_port_text_elem.text

                print('ip_port_text: "', ip_port_text, '"')

                ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip_port_text).group(0)
                port = re.search(r':\n(\d{2,5})', ip_port_text).group(1)

                if ip and port:
                    p = ProxyIP(ip=ip, port=port)
                    ip_list.append(p)

        return ip_list

    @staticmethod
    def should_render_js() -> bool:
        return True
