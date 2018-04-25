from scylla.providers import SpyMeProvider
from tests.providers.helpers import assert_provider


def test_spyme_provider():
    assert_provider(SpyMeProvider())
