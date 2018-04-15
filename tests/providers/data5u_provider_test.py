from scylla.providers import Data5uProvider
from tests.providers.helpers import assert_provider


def test_cool_proxy_provider():
    assert_provider(Data5uProvider())
