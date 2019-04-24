from scylla.providers.proxy_list_provider import ProxyListProvider
from tests.providers.helpers import assert_provider

def test_proxy_list_provider():
    assert_provider(ProxyListProvider())
