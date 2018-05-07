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

def _parse_str_to_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return 0


@app.route('/api/v1/proxies')
async def api_v1_proxies(request: Request):
    args = request.raw_args

    limit = 20

    page = 1

    is_anonymous = 2  # 0: no, 1: yes, 2: any

    if 'limit' in args:
        int_limit = _parse_str_to_int(args['limit'])
        limit = int_limit if int_limit else 20

    if 'page' in args:
        int_page = _parse_str_to_int(args['page'])
        page = int_page if int_page > 0 else 1

    if 'anonymous' in args:
        str_anonymous = args['anonymous']
        if str_anonymous == 'true':
            is_anonymous = 1
        elif str_anonymous == 'false':
            is_anonymous = 0
        else:
            is_anonymous = 2

    proxies = ProxyIP.select().where(ProxyIP.latency > 0).where(ProxyIP.latency < 9999) \
        .where(ProxyIP.is_valid == True)

    if is_anonymous != 2:
        if is_anonymous == 1:
            proxies = proxies.where(ProxyIP.is_anonymous == True)
        elif is_anonymous == 0:
            proxies = proxies.where(ProxyIP.is_anonymous == False)

    proxies = proxies.order_by(ProxyIP.updated_at.desc(), ProxyIP.latency).offset(page - 1).limit(limit)

    logger.debug('Perform SQL query: {}'.format(proxies.sql()))

    proxy_list = []

    for p in proxies:
        proxy_list.append(model_to_dict(p))

    return json({
        'proxies': proxy_list,
    })


def start_web_server(host='0.0.0.0', port=8000):
    app.run(host=host, port=port)
