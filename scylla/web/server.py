from playhouse.shortcuts import model_to_dict
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from sanic_cors import CORS

from scylla.database import ProxyIP
from scylla.loggings import logger

app = Sanic()

CORS(app)


# @app.route('/')
# async def test(request: Request):
#     return json({'hello': 'world', 'args': request.raw_args})


@app.route('/api/v1/proxies')
async def api_v1_proxies(request: Request):
    proxies = ProxyIP.select().where(ProxyIP.latency > 0).where(ProxyIP.latency < 9999) \
        .where(ProxyIP.is_valid == True) \
        .order_by(ProxyIP.updated_at.desc(), ProxyIP.latency).limit(20)

    logger.debug('Perform SQL query: ', proxies.sql())

    proxy_list = []

    for p in proxies:
        proxy_list.append(model_to_dict(p))

    return json({
        'proxies': proxy_list,
    })


def start_web_server(host='0.0.0.0', port=8000):
    app.run(host=host, port=port)
