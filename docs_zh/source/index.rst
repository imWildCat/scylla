Scylla 中文文档
==================================

.. toctree::
    :maxdepth: 2
    :caption: Contents:



Scylla 是一款高质量的免费代理 IP 池工具，仅支持 Python 3.6。特性如下：

-  自动化的代理 IP 爬取与验证
-  易用的 JSON API
-  简单但美观的 web 用户界面，基于 TypeScript 和 React（例如，代理的地理分布）
-  最少仅用\ **一条命令**\ 即可启动
-  简明直接的编程 API（将在 1.1 版本中加入）
-  最少仅用一行代码即可与 `Scrapy`_ 和 `requests`_ 进行集成
-  无头浏览器（headless browser crawling）爬虫

快速开始
--------

安装
"""""""

Docker 安装（推荐）
^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: shell

  docker run -d -p 8899:8899 -p 8081:8081 -v /var/www/scylla:/var/www/scylla --name scylla wildcat/scylla:latest

使用 pip 直接安装
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   pip install scylla
   scylla --help
   scylla # 运行爬虫和 Web 服务器

从源代码安装
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   git clone https://github.com/imWildCat/scylla.git
   cd scylla

   pip install -r requirements.txt

   npm install # 或 yarn install
   make build-assets

   python -m scylla

使用
"""""""

这里以服务运行在本地（``localhost``）为例，使用口号 ``8899``。
注意：首次运行本项目时，您可能需要等待 1～2 分钟以爬取一定量的代理 IP。

JSON API
^^^^^^^^^^^^^^^^^^

代理 IP 列表
~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    http://localhost:8899/api/v1/proxies

可选 URL 参数：

========= ======== ================================================================
参数       默认值    说明
========= ======== ================================================================
page      ``1``     页码
limit     ``20``    每页显示代理 IP 的数量
anonymous ``any``   是否显示匿名代理。可选值：``true``，只显示匿名代理；``false``，只显示透明代理。
https     ``any``   是否显示 HTTPS 代理。可选值：``true``，只显示 HTTPS 代理；``false``，只显示 HTTP 代理。
countries 无        只选取特定国家的代理，格式示例：``US``，或者多国家：``US,GB``
========= ======== ================================================================

结果样例：

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

系统统计
~~~~~~~~~~~~~~~~~

.. code:: shell

    http://localhost:8899/api/v1/stats

结果样例：

.. code:: json

    {
        "median": 181.2566407083,
        "valid_count": 1780,
        "total_count": 9528,
        "mean": 174.3290085201
    }

HTTP 正向代理服务器
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

默认情况下，Scylla 会在端口 ``8081`` 启动一个 HTTP 正向代理服务器（Forward Proxy Server）。
这个服务器会从数据库中选择一个刚更新过的代理，并将其用作正向代理。
每当发出 HTTP 请求时，代理服务器将随机选择一个代理。

注意：目前不支持 HTTPS 请求。

使用此代理服务器的 “curl” 示例如下：

.. code:: shell

    curl http://api.ipify.org -x http://127.0.0.1:8081

你也可以在 `requests`_ 中使用这个特性：

.. code:: python

    requests.get('http://api.ipify.org', proxies={'http': 'http://127.0.0.1:8081'})

Web 界面
^^^^^^^^^^^^^^^^^^

打开 ``http://localhost:8899`` 即可访问本项目的 Web 界面。

代理 IP 列表
~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    http://localhost:8899/

截图：

|screenshot-proxy-list|

代理 IP 全球分布
~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    http://localhost:8899/#/geo

截图：

|screenshot-geo-distribution|

API 文档
--------------

请阅读 :ref:`modindex`。更易用的编程接口正在开发中。

开发路线图
--------------

请查看 `Projects`_。

开发与贡献
----------------------------

.. code:: bash

   git clone https://github.com/imWildCat/scylla.git
   cd scylla

   pip install -r requirements.txt

   npm install # 或 `yarn install`
   make build-assets

测试
-------

本项目使用了较多的单元测试来保证代码的质量，并集成 `Travis CI`_ 来实现持续集成。如需在本地运行测试，命令如下：

.. code:: bash

   pip install -r tests/requirements-test.txt
   pytest tests/

十分欢迎您添加更多的测试用力以增强本项目的鲁棒性。

项目命名
--------------
`Scylla`_，或被称为“锡拉”（中文里），源自于美剧《`越狱`_》中的一组记忆芯片的名字。本项目以此命名，是为了致敬这部美剧。

捐助
----------------------
如果您认为这个项目有帮助，不妨为它捐助一点钱？

不管钱有多少，您的捐助将会激励作者持续开发新功能！🎉

感谢您的支持！

捐助方法如下：

PayPal
""""""
|PayPal Donation Official|

支付宝或微信
""""""""""""""""""""
|Alipay and WeChat Donation|

协议
-------

Apache License 2.0. 如需了解详情，请阅读 `LICENSE`_ 这个文件。


索引表
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Projects: https://github.com/imWildCat/scylla/projects
.. _LICENSE: https://github.com/imWildCat/scylla/blob/master/LICENSE
.. _Travis CI: https://travis-ci.org/imWildCat/scylla
.. _Scylla: http://prisonbreak.wikia.com/wiki/Scylla
.. _越狱: https://zh.wikipedia.org/zh-hans/%E8%B6%8A%E7%8B%B1_(%E7%94%B5%E8%A7%86%E5%89%A7)
.. _Scrapy: https://scrapy.org
.. _requests: http://docs.python-requests.org/

.. |screenshot-geo-distribution| image:: https://user-images.githubusercontent.com/2396817/40653599-9458b6b8-6333-11e8-8e6e-1d90271fc083.png
.. |screenshot-proxy-list| image:: https://user-images.githubusercontent.com/2396817/40653600-946eae6e-6333-11e8-8bbd-9d2f347c5461.png

.. |PayPal Donation Official| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5DXFA7WGWPZBN
.. |Alipay and WeChat Donation| image:: https://user-images.githubusercontent.com/2396817/40589594-cfb0e49e-61e7-11e8-8f7d-c55a29676c40.png
   :target: https://user-images.githubusercontent.com/2396817/40589594-cfb0e49e-61e7-11e8-8f7d-c55a29676c40.png  
