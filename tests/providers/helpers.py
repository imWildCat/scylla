import re
import time

import pytest

from scylla.providers import BaseProvider
from scylla.proxy_ip import ProxyIP
from scylla.worker import Worker


@pytest.fixture
def worker_instance():
    return Worker()


def _validate_ip(ip: str) -> bool:
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
        return True
    else:
        return False


def assert_provider(p: BaseProvider):
    w = worker_instance()

    urls = p.urls()

    for url in urls:
        html = w.get_html(url, p.should_render_js())

        proxy_list: [ProxyIP] = p.parse(html)

        assert len(proxy_list) > 0, 'Provider {} produce no ip'.format(p.__class__)

        for proxy in proxy_list:
            assert _validate_ip(proxy.ip) is True, 'Provider {} produce a proxy with an invalid ip: {}'.format(
                p.__class__, proxy.ip)
            assert 0 < proxy.port <= 65535, 'Provider {} produce a proxy with an invalid port: {}'.format(p.__class__,
                                                                                                          proxy.port)

        time.sleep(p.sleep_seconds())
