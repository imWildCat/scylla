from scylla.providers import FreeProxyListProvider
from .helpers import assert_provider


def test_free_proxy_list_provider():
    assert_provider(FreeProxyListProvider())
