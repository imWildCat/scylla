.. _requests_integration:

Example with Requests
=====================

`Requests`_ is a very nice and mature HTTP library for Python. To use Scylla with this library is very easy.

With the JSON API
-----------------

.. code:: python

    import requests
    import random

    json_resp = requests.get('http://localhost:8899/api/v1/proxies').json()
    proxy = random.choice(json_resp['proxies'])

    requests.get('http://api.ipify.org', proxies={'http': 'http://{}:{}'.format(proxy['ip'], proxy['port'])})

HTTPS proxy is also supported as well:

.. code:: python

    import requests
    import random

    json_resp = requests.get('http://localhost:8899/api/v1/proxies?https=true').json()
    proxy = random.choice(json_resp['proxies'])

    requests.get('https://api.ipify.org', proxies={'https': 'https://{}:{}'.format(proxy['ip'], proxy['port'])})




With the forward proxy server
-----------------------------

.. code:: python

    requests.get('http://api.ipify.org', proxies={'http': 'http://127.0.0.1:8081'})




.. _Requests: http://docs.python-requests.org/