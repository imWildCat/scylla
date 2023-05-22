from .base_provider import BaseProvider
from .free_proxy_list_provider import FreeProxyListProvider
from .ipaddress_provider import IpaddressProvider
from .proxy_list_provider import ProxyListProvider
from .proxy_scraper_provider import ProxyScraperProvider
from .proxylists_provider import ProxylistsProvider
from .proxynova_provider import ProxyNovaProvider
from .spys_me_provider import SpyMeProvider
from .spys_one_provider import SpysOneProvider
from .github_txt_provider import TheSpeedXProvider

all_providers = [
    FreeProxyListProvider,
    SpyMeProvider,
    SpysOneProvider,
    IpaddressProvider,
    ProxyListProvider,
    ProxyScraperProvider,
    ProxylistsProvider,
    ProxyNovaProvider,
    TheSpeedXProvider
]
