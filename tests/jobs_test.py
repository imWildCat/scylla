from scylla.database import ProxyIP
from scylla.jobs import validate_proxy_ip


def test_validate_proxy_ip(mocker):
    method = mocker.patch('scylla.validator.Validator.validate')
    p = ProxyIP(ip='127.0.0.1', port=80)
    validate_proxy_ip(p)
    method.assert_called_once()
