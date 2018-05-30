Scylla: An Intelligent Proxy Pool for Humanities™
==================================================

An intelligent proxy pool for humanities, only supports Python 3.6. Key
features:

-  Automatic proxy ip crawling and validation
-  Easy-to-use JSON API
-  Simple but beautiful web-based user interface (eg. geographical
   distribution of proxies)
-  Get started with only **1 command** minimally
-  Simple HTTP Forward proxy server
-  `Scrapy`_ and `requests`_ integration with only 1 line of code minimally
-  Headless browser crawling

对于偏好中文的用户，请阅读 `中文文档`_\ 。For those who prefer to use Chinese, please read the `Chinese Documentation`_


Get started
-----------

Installation
""""""""""""

Install with Docker (highly recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: shell

  docker run -d -p 8899:8899 -p 8081:8081 -v /var/www/scylla:/var/www/scylla --name scylla wildcat/scylla:latest

Install directly via pip
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   pip install scylla
   scylla --help
   scylla # Run the cralwer and web server for JSON API

Install from source
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   git clone https://github.com/imWildCat/scylla.git
   cd scylla

   pip install -r requirements.txt

   npm install # or yarn install
   make build-assets

   python -m scylla

Usage
"""""

This is an example of running a service locally (``localhost``), using port ``8899``.

Note: You might have to wait for 1 to 2 minutes in order to get some proxy ips populated in the database for the first time you use Scylla.

JSON API
^^^^^^^^^^^^^^^^^^

Proxy IP List
~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    http://localhost:8899/api/v1/proxies

Optional URL parameters:

========== ============= =================================================================
Parameters Default value Description
========== ============= =================================================================
page       ``1``         The page number
limit      ``20``        The number of proxies shown on each page
anonymous  ``any``       Show anonymous proxies or not. Possible values：``true``, only anonymous proxies; ``false``, only transparent proxies
https      ``any``       Show HTTPS proxies or not. Possible values：``true``, only HTTPS proxies; ``false``, only HTTP proxies
countries  None          Filter proxies for specific countries. Format example: ``US``, or multi-countries: ``US,GB``
========== ============= =================================================================

Sample result:

.. code:: json

    {
        "proxies": [{
            "id": 599,
            "ip": "91.229.222.163",
            "port": 53281,
            "is_valid": true,
            "created_at": 1527590947,
            "updated_at": 1527593751,
            "latency": 23.0,
            "stability": 0.1,
            "is_anonymous": true,
            "is_https": true,
            "attempts": 1,
            "https_attempts": 0,
            "location": "54.0451,-0.8053",
            "organization": "AS57099 Boundless Networks Limited",
            "region": "England",
            "country": "GB",
            "city": "Malton"
        }, {
            "id": 75,
            "ip": "75.151.213.85",
            "port": 8080,
            "is_valid": true,
            "created_at": 1527590676,
            "updated_at": 1527593702,
            "latency": 268.0,
            "stability": 0.3,
            "is_anonymous": true,
            "is_https": true,
            "attempts": 1,
            "https_attempts": 0,
            "location": "32.3706,-90.1755",
            "organization": "AS7922 Comcast Cable Communications, LLC",
            "region": "Mississippi",
            "country": "US",
            "city": "Jackson"
        },
        ...
        ],
        "count": 1025,
        "per_page": 20,
        "page": 1,
        "total_page": 52
    }

System Statistics
~~~~~~~~~~~~~~~~~

.. code:: shell

    http://localhost:8899/api/v1/stats

Sample result:

.. code:: json

    {
        "median": 181.2566407083,
        "valid_count": 1780,
        "total_count": 9528,
        "mean": 174.3290085201
    }

HTTP Forward Proxy Server
^^^^^^^^^^^^^^^^^^^^^^^^^

By default, Scylla will start a HTTP Forward Proxy Server on port ``8081``.
This server will select one proxy updated recently from the database and it will be used for forward proxy.
Whenever an HTTP request comes, the proxy server will select a proxy randomly.

Note: HTTPS requests are not supported at present.

The example for ``curl`` using this proxy server is shown below:

.. code:: shell

    curl http://api.ipify.org -x http://127.0.0.1:8081

You could also use this feature with `requests`_:

.. code:: python

    requests.get('http://api.ipify.org', proxies={'http': 'http://127.0.0.1:8081'})

Web UI
^^^^^^^^^^^^^^^^^^

Open ``http://localhost:8899`` in your browser to see the Web UI of this project.

Proxy IP List
~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    http://localhost:8899/

Screenshot:

|screenshot-proxy-list|

Globally Geographical Distribution Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    http://localhost:8899/#/geo

Screenshot:

|screenshot-geo-distribution|

Other Examples
--------------

.. toctree::
    :maxdepth: 1

    requests_integration

System Design
-------------

.. toctree::
    :maxdepth: 1

    validation_policy

API Documentation
-----------------

Please read :ref:`modindex`. 

Roadmap
--------------

Please see `Projects`_.

Development and Contribution
----------------------------

.. code:: bash

   git clone https://github.com/imWildCat/scylla.git
   cd scylla

   pip install -r requirements.txt

   npm install # or `yarn install`
   make build-assets

Testing
-------

If you wish to run tests locally, the commands are shown below:

.. code:: bash

   pip install -r tests/requirements-test.txt
   pytest tests/

You are welcomed to add more test cases to this project, increasing the robustness of this project.

Naming of This Project
----------------------
`Scylla`_ is derived from the name of a group of memory chips in the American TV series, `Prison Break`_. This project was named after this American TV series to pay tribute to it.

Donation
----------------------
If you find this project useful, could you please donate some money to it?

No matter how much the money is, Your donation will inspire the author to develop new features continuously! 🎉

Thank you!

The ways for donation are shown below:

PayPal
""""""
|PayPal Donation Official|

Alipay or WeChat Pay
""""""""""""""""""""
|Alipay and WeChat Donation|

License
-------

Apache License 2.0. For more details, please read the
`LICENSE`_ file.


.. _Projects: https://github.com/imWildCat/scylla/projects
.. _LICENSE: https://github.com/imWildCat/scylla/blob/master/LICENSE
.. _Travis CI: https://travis-ci.org/imWildCat/scylla
.. _Scylla: http://prisonbreak.wikia.com/wiki/Scylla
.. _Prison Break: https://en.wikipedia.org/wiki/Prison_Break
.. _中文文档: https://scylla.wildcat.io/zh/latest/
.. _Chinese Documentation: https://scylla.wildcat.io/zh/latest/
.. _Scrapy: https://scrapy.org
.. _requests: http://docs.python-requests.org/

.. |screenshot-geo-distribution| image:: https://user-images.githubusercontent.com/2396817/40653599-9458b6b8-6333-11e8-8e6e-1d90271fc083.png
.. |screenshot-proxy-list| image:: https://user-images.githubusercontent.com/2396817/40653600-946eae6e-6333-11e8-8bbd-9d2f347c5461.png

.. |PayPal Donation Official| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5DXFA7WGWPZBN
.. |Alipay and WeChat Donation| image:: https://user-images.githubusercontent.com/2396817/40589594-cfb0e49e-61e7-11e8-8f7d-c55a29676c40.png
   :target: https://user-images.githubusercontent.com/2396817/40589594-cfb0e49e-61e7-11e8-8f7d-c55a29676c40.png  

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
