from scylla.providers import IpaddressProvider
from .helpers import assert_provider


def test_ipaddress_provider():
    assert_provider(IpaddressProvider())
