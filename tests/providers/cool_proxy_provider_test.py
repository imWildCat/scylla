from scylla.providers import CoolProxyProvider
from tests.providers.helpers import assert_provider


def test_cool_proxy_provider():
    assert_provider(CoolProxyProvider())
