from scylla.providers.proxynova_provider import ProxyNovaProvider
from tests.providers.helpers import assert_provider

def test_proxynova_provider():
    assert_provider(ProxyNovaProvider())

