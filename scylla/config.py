from typing import Union

_config_data = {}


def _config_data_instance():
    global _config_data
    return _config_data


def set_config(key: str, value: str):
    _config_data_instance()[key] = value


def get_config(key: str, default: str = None) -> Union[str, None]:
    try:
        return _config_data_instance()[key]
    except KeyError:
        return default


def batch_set_config(**kwargs):
    for k, v in kwargs.items():
        set_config(k, v)
