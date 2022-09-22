import json

from pyquery import PyQuery

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class ProxyScraperProvider(BaseProvider):

    def urls(self) -> [str]:
        return ['https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json']

    def parse(self, document: PyQuery) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        text = document.html()
        json_object = json.loads(text)
        if not json_object or type(json_object['proxynova']) != list:
            return ip_list

        for ip_port in json_object['proxynova']:
            p = ProxyIP(ip=ip_port['ip'], port=ip_port['port'])
            ip_list.append(p)

        return ip_list

    @staticmethod
    def should_render_js() -> bool:
        return False
