from scylla.providers.proxy_scraper_provider import ProxyScraperProvider
from tests.providers.helpers import assert_provider


def test_proxy_scraper_provider():
    assert_provider(ProxyScraperProvider())
