from scylla.providers import A2uProvider
from tests.providers.helpers import assert_provider


def test_a2u_provider():
    assert_provider(A2uProvider())
