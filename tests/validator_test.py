import pytest

from scylla.validator import Validator


@pytest.fixture
def validator():
    return Validator(host='145.239.185.126', port=1080)


@pytest.fixture
def validator2():
    return Validator(host='162.246.200.100', port=80)


def test_latency(validator):
    validator.validate_latency()
    assert validator.success_rate >= 0
    # TODO: fix the problem of latency == 0
    assert validator.latency >= 0


def test_proxy(validator):
    validator.validate_proxy()


def test_proxy(validator2):
    validator2.validate_proxy()


def test_proxy(validator2, mocker):
    l = mocker.patch('scylla.validator.Validator.validate_latency')
    p = mocker.patch('scylla.validator.Validator.validate_proxy')
    validator2.validate()
    l.assert_called_once()
    p.assert_called_once()
