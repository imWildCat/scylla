import base64
import re
from typing import List

from pyquery import PyQuery

from scylla.database import ProxyIP
from scylla.worker import Worker
from .base_provider import BaseProvider
import urllib.parse

class ProxyListProvider(BaseProvider):

    def __init__(self):
        super().__init__()
        self.w = Worker()

    def parse(self, document: PyQuery) -> List[ProxyIP]:
        ip_list: List[ProxyIP] = []

        if document is None:
            return []

        for ul in document('#proxy-table > div.table-wrap ul').items():
            js_code_element = ul.find('li.proxy script')

            if not js_code_element:
                return []

            js_code = js_code_element.text()
            matched = re.findall(r"Proxy\('(.+)'\)", js_code)
            if matched and len(matched) > 0:
                encoded = matched[0]
                ip_port = base64.b64decode(encoded).decode("utf-8")
                ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip_port)[0]
                port = re.findall(r':(\d{2,5})', ip_port)[0]
                ip_list.append(ProxyIP(ip=ip, port=port))

        return ip_list

    def urls(self) -> List[str]:
        ret = []
        first_url = 'http://proxy-list.org/english/index.php?p=1'
        first_page = self.w.get_html(first_url, False)
        if first_page:
            ret.append(first_url)
            for a in first_page.find('#content div.content div.table-menu a.item'):
                relative_path = a.attrib['href']
                absolute_url = urllib.parse.urljoin(first_url, relative_path)
                ret.append(absolute_url)
        return ret


    @staticmethod
    def should_render_js() -> bool:
        return False

