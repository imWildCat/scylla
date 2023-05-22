import re

import js2py as js2py
from pyquery import PyQuery

from scylla.database import ProxyIP
from scylla.worker import Worker
from .base_provider import BaseProvider


class ProxylistsProvider(BaseProvider):

    def __init__(self):
        super().__init__()
        self.w = Worker()
        self.country_patten = re.compile('^/(.+)_0.html$')

    def parse(self, document: PyQuery) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for tr in document('table table tr').items():
            tr: PyQuery = tr
            ip_element = tr.find('td:nth-of-type(1)')
            port_element = tr.find('td:nth-of-type(2)')
            ipexec = ip_element.text().replace("Click here to view proxy check date, country and type", "").replace(
                "eval(", "").replace("Please enable javascript", "").replace(");", "").strip()
            if ip_element and port_element:
                ip_element = js2py.eval_js(ipexec)
                ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip_element).group(0)
                port = re.search(r'\d{2,5}', port_element.text()).group(0)
                ip_list.append(ProxyIP(ip=ip, port=port))

        return ip_list

    def urls(self) -> [str]:
        ret = set([])
        country_url = 'http://www.proxylists.net/countries.html'
        country_page = self.w.get_html(country_url, False)
        if country_page:
            for a in country_page.find('a'):
                relative_path = a.attrib['href']
                if self.country_patten.match(relative_path):
                    ret.update(self.gen_url_for_country(self.country_patten.findall(relative_path)[0]))
                    break
        return list(ret)

    def gen_url_for_country(self, country) -> [str]:
        ret = []
        first_page = self.w.get_html('http://www.proxylists.net/{}_0.html'.format(country), False)
        for a in first_page.find('table table tr:last-of-type a'):
            ret.append('http://www.proxylists.net/{}'.format(a.attrs['href']))
        return ret

    @staticmethod
    def should_render_js() -> bool:
        return True
