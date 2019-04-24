import json

from requests_html import HTML

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class ProxyScraperProvider(BaseProvider):

    def urls(self) -> [str]:
        return ['https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json']

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        text = html.raw_html.decode('utf-8')
        obj = json.loads(text)
        if not obj or type(obj['usproxy']) != list:
            return ip_list

        for ip_port in obj['usproxy']:
            p = ProxyIP(ip=ip_port['ip'], port=ip_port['port'])
            ip_list.append(p)

        return ip_list

    @staticmethod
    def should_render_js() -> bool:
        return False
