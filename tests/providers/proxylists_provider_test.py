from scylla.providers.proxylists_provider import ProxylistsProvider
from tests.providers.helpers import assert_provider


def test_proxylists_provider():
    assert_provider(ProxylistsProvider())


