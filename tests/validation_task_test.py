import pytest

from scylla.database import ProxyIP
from scylla.validation_task import ValidationTask


@pytest.fixture
def proxy_ip():
    return ProxyIP(ip='127.0.0.1', port=3306, latency=200.00, stability=100.0, is_valid=True)


def test_validation_task(proxy_ip):
    vt = ValidationTask(proxy_ip=proxy_ip)

    assert vt.proxy_ip.ip == '127.0.0.1'

    assert vt.num_of_attempts == 0

    vt.increase_num_of_attempts()

    assert vt.num_of_attempts == 1
