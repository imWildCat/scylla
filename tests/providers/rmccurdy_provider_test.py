from scylla.providers.rmccurdy_provider import RmccurdyProvider
from tests.providers.helpers import assert_provider


def test_rmcurrdy_provider():
    assert_provider(RmccurdyProvider())
