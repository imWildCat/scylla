![banner_scylla](https://user-images.githubusercontent.com/2396817/40580477-f15a15b8-6136-11e8-9f4b-1f012e90712c.png) [![Build Status](https://travis-ci.org/imWildCat/scylla.svg?branch=master)](https://travis-ci.org/imWildCat/scylla) [![codecov](https://codecov.io/gh/imWildCat/scylla/branch/master/graph/badge.svg)](https://codecov.io/gh/imWildCat/scylla) [![Documentation Status](https://readthedocs.org/projects/scylla-py/badge/?version=latest)](https://scylla.wildcat.io/en/latest/?badge=latest) [![PyPI version](https://badge.fury.io/py/scylla.svg)](https://badge.fury.io/py/scylla) [![Docker Build Status](https://img.shields.io/docker/build/wildcat/scylla.svg)](https://hub.docker.com/r/wildcat/scylla/) 
===

An intelligent proxy pool for humanities, only supports Python 3.6. Key
features:

- Automatic proxy ip crawling and validation
- Easy-to-use JSON API
- Simple but beautiful web-based user interface (eg. geographical
    distribution of proxies)
- Get started with only **1 command** minimally
- Straightforward programmable API
- Headless browser crawling

对于偏好中文的用户，请阅读
[中文文档](https://scylla.wildcat.io/zh/latest/)。For those who prefer
to use Chinese, please read the [Chinese
Documentation](https://scylla.wildcat.io/zh/latest/).

Get started
===========

Installation
------------

### Install with Docker (highly recommended)

```bash
$ docker run -d -p 8899:8899 -v /var/www/scylla:/var/www/scylla --name scylla wildcat/scylla:latest
```

### Install directly via pip

```bash
pip install scylla
scylla --help
scylla # Run the cralwer and web server for JSON API
```

### Install from source

```bash
git clone https://github.com/imWildCat/scylla.git
cd scylla

pip install -r requirements.txt

npm install # or yarn install
make build-assets

python -m scylla
```

Usage
-----

This is an example of running a service locally (`localhost`), using
port `8899`.

Note: You might have to wait for 1 to 2 minutes in order to wait for the
crawler get some proxy ips for the first time you use Scylla.

### JSON API

#### Proxy IP List

```bash
http://localhost:8899/api/v1/proxies
```

Optional URL parameters:

| Parameters | Default value | Description                                                                                                       |
|------------|---------------|-------------------------------------------------------------------------------------------------------------------|
| page       | `1`           | The page number                                                                                                   |
| limit      | `20`          | The number of proxies shown on each page                                                                          |
| anonymous  | `any`         | Show anonymous proxies or not. Possible values：`true`, only anonymous proxies; `false`, only transparent proxies |

Sample result:

```json
{
    "proxies": [{
        "id": 3661,
        "ip": "118.114.77.47",
        "port": 8080,
        "is_valid": true,
        "created_at": 1527312259,
        "updated_at": 1527351023,
        "latency": 250.9789636882,
        "stability": 1.0,
        "is_anonymous": true,
        "location": "29.3416,104.7770",
        "organization": "AS4134 CHINANET-BACKBONE",
        "region": "Sichuan",
        "country": "CN",
        "city": "Zigong"
    }, {
        "id": 3657,
        "ip": "39.104.57.121",
        "port": 8080,
        "is_valid": true,
        "created_at": 1527312253,
        "updated_at": 1527351021,
        "latency": 189.1011954867,
        "stability": 0.2,
        "is_anonymous": true,
        "location": null,
        "organization": null,
        "region": null,
        "country": null,
        "city": null
    },
    ...
    ],
    "count": 1025,
    "per_page": 20,
    "page": 1,
    "total_page": 52
}
```

#### System Statistics

```bash
http://localhost:8899/api/v1/stats
```

Sample result:

```json
{
    "median": 181.2566407083,
    "valid_count": 1780,
    "total_count": 9528,
    "mean": 174.3290085201
}
```

### Web UI

Open `http://localhost:8899` in your browser to see the Web UI of this
project.

#### Proxy IP List

```
http://localhost:8899/
```

Screenshot:

![screenshot-proxy-list](https://user-images.githubusercontent.com/2396817/40578443-13bcbbd6-610c-11e8-85d5-1a11b66bf5d4.png)

#### Globally Geographical Distribution Map

```
http://localhost:8899/#/geo
```

Screenshot:

![screenshot-geo-distribution](https://user-images.githubusercontent.com/2396817/40578442-13a8491c-610c-11e8-8340-50097f29fdad.png)

API Documentation
=================

Please read [Module
Index](https://scylla.wildcat.io/en/latest/py-modindex.html).

Roadmap
=======

Please see [Projects](https://github.com/imWildCat/scylla/projects).

Development and Contribution
============================

```bash
git clone https://github.com/imWildCat/scylla.git
cd scylla

pip install -r requirements.txt

npm install # or `yarn install`
make build-assets
```

Testing
=======

If you wish to run tests locally, the commands are shown below:

```bash
pip install -r tests/requirements-test.txt
pytest -n 15 tests
```

You are welcomed to add more test cases to this project, increasing the
robustness of this project.

Naming of This Project
======================

[Scylla](http://prisonbreak.wikia.com/wiki/Scylla) is derived from the
name of a group of memory chips in the American TV series, [Prison
Break](https://en.wikipedia.org/wiki/Prison_Break). This project was
named after this American TV series to pay tribute to it.

License
=======

Apache License 2.0. For more details, please read the
[LICENSE](https://github.com/imWildCat/scylla/blob/master/LICENSE) file.
