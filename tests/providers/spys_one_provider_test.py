from scylla.providers import SpysOneProvider
from tests.providers.helpers import assert_provider


def test_cool_proxy_provider():
    assert_provider(SpysOneProvider())
