import re

from requests_html import HTML

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class ProxyNovaProvider(BaseProvider):

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for tr in html.find('#tbl_proxy_list > tbody:nth-child(2) > tr'):
            if not 'data-proxy-id' in tr.attrs:
                continue

            script_element = tr.find('td:nth-child(1) > abbr > script', first=True)
            port_element = tr.find('td:nth-child(2)', first=True)
            if not script_element or not port_element:
                continue

            groups = re.findall(r"document\.write\('12345678(\d{1,3}\.\d{1,3})'\.substr\(8\) \+ '(\d{1,3}\.\d{1,3}\.\d{1,3})'\)", script_element.text)
            if not groups or len(groups) != 1:
                continue
            ip = groups[0][0] + groups[0][1]
            port = port_element.text
            ip_list.append(ProxyIP(ip=ip, port=port))
        return ip_list

    def urls(self) -> [str]:
        return ['https://www.proxynova.com/proxy-server-list/']

    @staticmethod
    def should_render_js() -> bool:
        return False

