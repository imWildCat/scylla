import base64
import re

from requests_html import HTML

from scylla.database import ProxyIP
from scylla.worker import Worker
from .base_provider import BaseProvider


class ProxyListProvider(BaseProvider):

    def __init__(self):
        self.w = Worker()

    def parse(self, html: HTML) -> [ProxyIP]:
        ip_list: [ProxyIP] = []

        for ul in html.find('#proxy-table > div.table-wrap ul'):
            js_code = ul.find('li.proxy script', first=True).text
            matched = re.findall(r"Proxy\('(.+)'\)", js_code)
            if matched and len(matched) > 0:
                encoded = matched[0]
                ip_port = base64.b64decode(encoded).decode("utf-8")
                ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip_port)[0]
                port = re.findall(r':(\d{2,5})', ip_port)[0]
                ip_list.append(ProxyIP(ip=ip, port=port))

        return ip_list

    def urls(self) -> [str]:
        ret = []
        first_url = 'http://proxy-list.org/english/index.php?p=1'
        sub = first_url[0:first_url.rfind('/')] # http://proxy-list.org/english
        first_page = self.w.get_html(first_url, False)

        ret.append(first_url)
        for a in first_page.find('#content div.content div.table-menu a.item'):
            relative_path = a.attrs['href']
            absolute_url = sub + relative_path[relative_path.find('/'):]
            ret.append(absolute_url)
        return ret


    @staticmethod
    def should_render_js() -> bool:
        return False

