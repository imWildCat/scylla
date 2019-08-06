from scylla.database import ProxyIP
from scylla.jobs import validate_proxy_ip, save_ip


def test_validate_proxy_ip(mocker):
    method = mocker.patch('scylla.validator.Validator.validate')
    method2 = mocker.patch('scylla.jobs.save_ip')
    p = ProxyIP(ip='127.0.0.1', port=80)
    validate_proxy_ip(p)
    method.assert_called_once()
    method2.assert_called_once()


def test_save_ip():
    p1 = ProxyIP(ip='192.168.0.1', port=443, latency=200, stability=0.5)
    save_ip(p1)
    # basically the same ip
    p2 = ProxyIP(ip='192.168.0.1', port=443, latency=200, stability=0.5)
    save_ip(p2)
    count = ProxyIP.select().where(ProxyIP.ip == '192.168.0.1').count()

    assert count == 1

    p3 = ProxyIP(ip='192.168.0.1', port=80, latency=200, stability=0.5)
    save_ip(p3)
    count = ProxyIP.select().where(ProxyIP.ip == '192.168.0.1').count()

    assert count == 2

    ProxyIP.delete().execute()
