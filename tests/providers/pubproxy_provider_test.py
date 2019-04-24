from scylla.providers.pubproxy_provider import PubproxyProvider
from tests.providers.helpers import assert_provider


def test_pubproxy_provider():
    assert_provider(PubproxyProvider())
