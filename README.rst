|Scylla Banner| |Build Status| |codecov| |Documentation Status| |PyPI version| |Docker Build Status| |PayPal Donation|
==============================================================================================================================================

An intelligent proxy pool for humanities, only supports Python 3.6. Key features:

-  Automatic proxy ip crawling and validation
-  Easy-to-use JSON API
-  Simple but beautiful web-based user interface (eg. geographical
   distribution of proxies)
-  Get started with only **1 command** minimally
-  Simple HTTP Forward proxy server
-  `Scrapy`_ and `requests`_ integration with only 1 line of code minimally
-  Headless browser crawling

对于偏好中文的用户，请阅读 `中文文档`_\ 。For those who prefer to use Chinese, please read the `Chinese Documentation`_

Documentation
-------------

Please read the `Documentation`_. 

Quick start
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
   scylla # Run the crawler and web server for JSON API

Install from source
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

   git clone https://github.com/imWildCat/scylla.git
   cd scylla

   pip install -r requirements.txt

   npm install # or yarn install
   make assets-build

   python -m scylla

For Windows user who fails at installing ``sanic`` due to ``uvloop does not support Windows at the moment``:

.. code:: bash

   export SANIC_NO_UVLOOP=true
   export SANIC_NO_UJSON=true
   pip3 install sanic

If this also fails, yoi will need to manual install sanic from source.


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
   make assets-build

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

.. _Module Index: https://scylla.wildcat.io/en/latest/py-modindex.html
.. _Projects: https://github.com/imWildCat/scylla/projects
.. _LICENSE: https://github.com/imWildCat/scylla/blob/master/LICENSE
.. _Travis CI: https://travis-ci.org/imWildCat/scylla
.. _Scylla: http://prisonbreak.wikia.com/wiki/Scylla
.. _Prison Break: https://en.wikipedia.org/wiki/Prison_Break
.. _中文文档: https://scylla.wildcat.io/zh/latest/
.. _Chinese Documentation: https://scylla.wildcat.io/zh/stable/
.. _Documentation: https://scylla.wildcat.io/en/stable/
.. _Scrapy: https://scrapy.org
.. _requests: http://docs.python-requests.org/


.. |Scylla Banner| image:: https://user-images.githubusercontent.com/2396817/40580477-f15a15b8-6136-11e8-9f4b-1f012e90712c.png
.. |Build Status| image:: https://travis-ci.org/imWildCat/scylla.svg?branch=master
   :target: https://travis-ci.org/imWildCat/scylla
.. |codecov| image:: https://codecov.io/gh/imWildCat/scylla/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/imWildCat/scylla
.. |Documentation Status| image:: https://readthedocs.org/projects/scylla-py/badge/?version=latest
   :target: https://scylla.wildcat.io/en/latest/?badge=latest
.. |PyPI version| image:: https://badge.fury.io/py/scylla.svg
   :target: https://badge.fury.io/py/scylla
.. |Docker Build Status| image:: https://img.shields.io/docker/build/wildcat/scylla.svg
   :target: https://hub.docker.com/r/wildcat/scylla/
.. |PayPal Donation| image:: https://img.shields.io/badge/Donate-PayPal-green.svg
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5DXFA7WGWPZBN
.. |PayPal Donation Official| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=5DXFA7WGWPZBN
.. |Alipay and WeChat Donation| image:: https://user-images.githubusercontent.com/2396817/40589594-cfb0e49e-61e7-11e8-8f7d-c55a29676c40.png
   :target: https://user-images.githubusercontent.com/2396817/40589594-cfb0e49e-61e7-11e8-8f7d-c55a29676c40.png  
