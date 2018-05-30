.. _requests_integration:

Requests 的一些例子
==========================

`Requests`_ 是一个非常好用而且成熟的 Python HTTP 框架。和它一起使用 Scylla 非常简单。

调用 JSON API
-----------------

.. code:: python

    import requests
    import random

    json_resp = requests.get('http://localhost:8899/api/v1/proxies').json()
    proxy = random.choice(json_resp['proxies'])

    requests.get('http://api.ipify.org', proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})

也支持 HTTPS 代理：

.. code:: python

    import requests
    import random

    json_resp = requests.get('http://localhost:8899/api/v1/proxies?https=true').json()
    proxy = random.choice(json_resp['proxies'])

    requests.get('https://api.ipify.org', proxies={'https': 'https://{}:{}'.format(proxy['ip'], proxy['port'])})




使用正向代理服务器
-----------------------------

.. code:: python

    requests.get('http://api.ipify.org', proxies={'http': 'http://127.0.0.1:8081'})




.. _Requests: http://docs.python-requests.org/