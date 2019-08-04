from scylla.providers.the_speedX_provider import TheSpeedXProvider
from tests.providers.helpers import assert_provider

def test_the_speedX_provider():
    assert_provider(TheSpeedXProvider())
