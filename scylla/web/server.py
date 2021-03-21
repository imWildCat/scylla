import math
import os

from playhouse.shortcuts import model_to_dict
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from sanic_cors import CORS

from scylla.database import ProxyIP
from scylla.loggings import logger

app = Sanic(name='Scylla', )

CORS(app)

base_path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

app.static('/assets/*', base_path + '/assets')
app.static('/', base_path + '/assets/index.html')
app.static('/*', base_path + '/assets/index.html')


def _parse_str_to_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return 0


def _get_valid_proxies_query():
    return ProxyIP.select().where(ProxyIP.latency > 0).where(ProxyIP.latency < 9999) \
        .where(ProxyIP.is_valid == True)


@app.route('/api/v1/proxies')
async def api_v1_proxies(request: Request):
    args = request.args

    limit = 20

    page = 1

    is_anonymous = 2  # 0: no, 1: yes, 2: any

    if 'limit' in args:
        int_limit = _parse_str_to_int(args.get('limit'))
        limit = int_limit if int_limit else 20

    if 'page' in args:
        int_page = _parse_str_to_int(args.get('page'))
        page = int_page if int_page > 0 else 1

    if 'anonymous' in args:
        str_anonymous = args.get('anonymous')
        if str_anonymous == 'true':
            is_anonymous = 1
        elif str_anonymous == 'false':
            is_anonymous = 0
        else:
            is_anonymous = 2

    str_https = None
    if 'https' in args:
        str_https = args.get('https')

    country_list = []
    if 'countries' in args:
        countries = args.get('countries')
        country_list = countries.split(',')

    proxy_initial_query = _get_valid_proxies_query()

    proxy_query = proxy_initial_query

    if is_anonymous != 2:
        if is_anonymous == 1:
            proxy_query = proxy_initial_query.where(ProxyIP.is_anonymous == True)
        elif is_anonymous == 0:
            proxy_query = proxy_initial_query.where(ProxyIP.is_anonymous == False)

    if str_https:
        if str_https == 'true':
            proxy_query = proxy_initial_query.where(ProxyIP.is_https == True)
        elif str_https == 'false':
            proxy_query = proxy_initial_query.where(ProxyIP.is_https == False)

    if country_list and len(country_list) > 0:
        proxy_query = proxy_query.where(ProxyIP.country << country_list)

    count = proxy_query.count()  # count before sorting

    proxies = proxy_query.order_by(ProxyIP.updated_at.desc(), ProxyIP.latency).offset((page - 1) * limit).limit(limit)

    logger.debug('Perform SQL query: {}'.format(proxy_query.sql()))

    proxy_list = []

    for p in proxies:
        dict_model = model_to_dict(p)
        dict_model['created_at'] = dict_model['created_at'].isoformat()
        dict_model['updated_at'] = dict_model['updated_at'].isoformat()
        proxy_list.append(
            dict_model
        )

    return json({
        'proxies': proxy_list,
        'count': count,
        'per_page': limit,
        'page': page,
        'total_page': math.ceil(count / limit),
    })


@app.route('/api/v1/stats')
async def api_v1_stats(request: Request):
    median_query: ProxyIP = ProxyIP.raw("""SELECT latency
                                FROM proxy_ips
                                WHERE is_valid = 1
                                ORDER BY latency
                                LIMIT 1
                                OFFSET (
                                  SELECT COUNT(*) FROM proxy_ips WHERE is_valid = 1
                                ) / 2""").get()
    median = median_query.latency

    mean_query: ProxyIP = ProxyIP.raw("""SELECT AVG(latency) as latency
                                    FROM proxy_ips
                                    WHERE is_valid = 1 AND latency < 9999""").get()
    mean = mean_query.latency

    valid_count = _get_valid_proxies_query().count()

    total_count = ProxyIP.select().count()

    return json({
        'median': median,
        'valid_count': valid_count,
        'total_count': total_count,
        'mean': mean,
    })


def start_web_server(host='0.0.0.0', port=8899):
    app.run(host=host, port=port)
