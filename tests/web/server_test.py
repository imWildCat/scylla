# import random

# import pytest
# from requests import Response
# from sanic.websocket import WebSocketProtocol
# from sanic import Sanic

# from scylla.web.server import app
# from ..database_test import create_test_ip, delete_test_ip, delete_test_ips, gen_random_ip, ProxyIP

# COUNTRIES = ['CN', 'US', 'GB']

# Sanic.test_mode = True

# @pytest.fixture
# def web_app():
#     return app


# @pytest.fixture
# def test_cli(loop, web_app, test_client):
#     return loop.run_until_complete(test_client(web_app, protocol=WebSocketProtocol))


# def populate_proxy_ips_in_db() -> [str]:
#     ips = []

#     anonymous = [True, False]

#     https = anonymous

#     for _ in range(0, 31):
#         ip_str = gen_random_ip()
#         ips.append(ip_str)

#         country = random.choice(COUNTRIES)
#         is_anonymous = random.choice(anonymous)
#         is_https = random.choice(https)

#         ip = ProxyIP(
#             ip=ip_str, port=3306, latency=200.00, stability=100.0, is_valid=True,
#             country=country, is_anonymous=is_anonymous, is_https=is_https,
#         )
#         ip.save()

#     return ips


# async def test_fixture_test_client_get(test_cli):
#     resp = await test_cli.get('/api/v1/proxies')
#     assert resp.status_code == 200


# async def test_get_proxies(test_cli):
#     ip_str = create_test_ip()

#     resp: Response = await test_cli.get('/api/v1/proxies')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     proxies = resp_json['proxies']
#     assert (len(proxies) > 0)

#     delete_test_ip(ip_str)


# async def test_get_proxies_limit(test_cli):
#     ip_str = create_test_ip()

#     resp = await test_cli.get('/api/v1/proxies?limit=10')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     proxies = resp_json['proxies']
#     assert (len(proxies) > 0)

#     delete_test_ip(ip_str)


# async def test_get_proxies_anonymous_true(test_cli):
#     ips = populate_proxy_ips_in_db()

#     resp = await test_cli.get('/api/v1/proxies?anonymous=true')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     proxies = resp_json['proxies']
#     assert len(proxies) > 0

#     for p in proxies:
#         assert p['is_anonymous'] == True

#     delete_test_ips(ips)


# async def test_get_proxies_anonymous_false(test_cli):
#     ips = populate_proxy_ips_in_db()

#     resp = await test_cli.get('/api/v1/proxies?anonymous=false')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     proxies = resp_json['proxies']
#     assert len(proxies) > 0

#     for p in proxies:
#         assert p['is_anonymous'] == False

#     delete_test_ips(ips)


# async def test_get_proxies_https_true(test_cli):
#     ips = populate_proxy_ips_in_db()

#     resp = await test_cli.get('/api/v1/proxies?https=true')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     proxies = resp_json['proxies']
#     assert len(proxies) > 0

#     for p in proxies:
#         assert p['is_https'] == True

#     delete_test_ips(ips)


# async def test_get_proxies_https_false(test_cli):
#     ips = populate_proxy_ips_in_db()

#     resp = await test_cli.get('/api/v1/proxies?https=false')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     proxies = resp_json['proxies']
#     assert len(proxies) > 0

#     for p in proxies:
#         assert p['is_https'] == False

#     delete_test_ips(ips)


# async def test_get_proxies_filtering_countries(test_cli):
#     ips = populate_proxy_ips_in_db()

#     resp = await test_cli.get('/api/v1/proxies?countries=CN')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     proxies = resp_json['proxies']

#     for p in proxies:
#         assert p['country'] == 'CN'

#     delete_test_ips(ips)


# async def test_get_proxies_filtering_multi_countries(test_cli):
#     ips = populate_proxy_ips_in_db()

#     resp = await test_cli.get('/api/v1/proxies?countries=CN,US')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     proxies = resp_json['proxies']

#     for p in proxies:
#         assert p['country'] == 'CN' or p['country'] == 'US'

#     delete_test_ips(ips)


# async def test_get_proxies_page(test_cli):
#     ips = populate_proxy_ips_in_db()

#     resp = await test_cli.get('/api/v1/proxies?page=2')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     proxies = resp_json['proxies']
#     assert len(proxies) > 0

#     delete_test_ips(ips)


# async def test_get_proxies_page_invalid(test_cli):
#     ip_str = create_test_ip()

#     resp = await test_cli.get('/api/v1/proxies?page=invalid')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     proxies = resp_json['proxies']
#     assert len(proxies) > 0

#     delete_test_ip(ip_str)


# async def test_get_stats(test_cli):
#     ip_str = create_test_ip()

#     resp = await test_cli.get('/api/v1/stats')
#     assert resp.status_code == 200

#     resp_json = resp.json()

#     assert resp_json['median']
#     assert resp_json['mean']
#     assert resp_json['valid_count']
#     assert resp_json['total_count']

#     delete_test_ip(ip_str)
