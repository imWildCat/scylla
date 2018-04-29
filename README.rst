Scylla |Build Status| |codecov| |Documentation Status| |PyPI version|
=====================================================================

A minimal proxy ip crawler, only supports Python 3.6.

Get started
-----------

Install directly via pip
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    pip install scylla
    scylla # Run the cralwer and web server for JSON API

Use from source
~~~~~~~~~~~~~~~

.. code:: bash

    git clone https://github.com/imWildCat/scylla.git
    cd scylla
    python -m scylla

Usage
-----

Standalone
~~~~~~~~~~

For more details, please read the `API
Documentation <http://scylla.wildcat.io/en/latest/py-modindex.html>`__.

Roadmap
-------

-  [x] Basic RESTFul API
-  [ ] Advanced RESTFul API (Sorting, paging, conditions)
-  [ ] Programmable API
-  [ ] Geographical distribution map for proxies
-  [ ] Docker integration
-  [ ] Smart web proxy server
-  [ ] More statistical views of proxies
-  [ ] Quality statistics for different providers

License
-------

Apache License 2.0. For more details, please read the
`LICENSE <./LICENSE>`__ file.

.. |Build Status| image:: https://travis-ci.org/imWildCat/scylla.svg?branch=master
   :target: https://travis-ci.org/imWildCat/scylla
.. |codecov| image:: https://codecov.io/gh/imWildCat/scylla/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/imWildCat/scylla
.. |Documentation Status| image:: https://readthedocs.org/projects/scylla-py/badge/?version=latest
   :target: http://scylla.wildcat.io/en/latest/?badge=latest
.. |PyPI version| image:: https://badge.fury.io/py/scylla.svg
   :target: https://badge.fury.io/py/scylla
