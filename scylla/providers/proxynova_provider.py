import js2py as js2py
from pyquery import PyQuery

from scylla.database import ProxyIP
from .base_provider import BaseProvider


class ProxyNovaProvider(BaseProvider):

    def parse(self, document: PyQuery) -> [ProxyIP]:
        ip_list: [ProxyIP] = []
        for tr in document('#tbl_proxy_list > tbody:nth-child(2) > tr').items():
            tr: PyQuery = tr

            if not tr.attr('data-proxy-id'):
                continue

            script_element = tr.find('td:nth-child(1) > abbr').text()
            port_element = tr.find('td:nth-child(2)')

            if not script_element or not port_element:
                continue

            script_element = 'let x = %s; x' % (script_element[15:-2])
            ip = js2py.eval_js(script_element).strip()
            port = port_element.text()
            ip_list.append(ProxyIP(ip=ip, port=port))

        return ip_list

    def urls(self) -> [str]:
        return ['https://www.proxynova.com/proxy-server-list/']

    @staticmethod
    def should_render_js() -> bool:
        return False
