from scylla.providers.comp0_provider import Comp0Provider
from tests.providers.helpers import assert_provider


def test_comp0_provider():
    assert_provider(Comp0Provider())
