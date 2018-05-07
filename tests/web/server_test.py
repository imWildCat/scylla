import pytest
from sanic.websocket import WebSocketProtocol

from scylla.web.server import app
from ..database_test import create_test_ip, delete_test_ip


@pytest.yield_fixture
def web_app():
    return app


@pytest.fixture
def test_cli(loop, web_app, test_client):
    return loop.run_until_complete(test_client(web_app, protocol=WebSocketProtocol))


async def test_fixture_test_client_get(test_cli):
    resp = await test_cli.get('/api/v1/proxies')
    assert resp.status == 200


async def test_get_proxies(test_cli):
    ip_str = create_test_ip()

    resp = await test_cli.get('/api/v1/proxies')
    assert resp.status == 200

    resp_json = await resp.json()

    proxies = resp_json['proxies']
    assert (len(proxies) > 0)

    delete_test_ip(ip_str)
