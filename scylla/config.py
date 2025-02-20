from typing import Union
from enum import Enum

class GeoIPAPI(Enum):
    IPSB = "ip.sb"
    IPQUERY = "ipquery.io"

_config_data = {
    "geoip_api": GeoIPAPI.IPSB
}

def _config_data_instance():
    global _config_data
    return _config_data

def set_config(key: str, value: Union[str, GeoIPAPI]):
    if key == "geoip_api" and isinstance(value, str):
        value = GeoIPAPI(value)
    _config_data_instance()[key] = value

def get_config(key: str, default: Union[str, GeoIPAPI] = None) -> Union[str, GeoIPAPI, None]:
    try:
        return _config_data_instance()[key]
    except KeyError:
        return default

def batch_set_config(**kwargs):
    for k, v in kwargs.items():
        set_config(k, v)
