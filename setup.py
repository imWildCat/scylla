import io
import os
from mock import Mock as MagicMock


from setuptools import setup

import scylla

here = os.path.abspath(os.path.dirname(__file__))
# Import the README and use it as the long-description.
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


# Re: https://github.com/dabercro/OpsSpace/blob/880c58f6a6172924ca03145916f6a27cf6633684/docs/conf.py
class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return Mock()


MOCK_MODULES = ['pycurl', ]
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

setup(
    name='scylla',
    python_requires='>=3.6.0',
    # If your package is a single module, use this instead of 'packages':
    packages=[
        'scylla',
        'scylla.providers',
        'scylla.web'
    ],
    entry_points={
        'console_scripts': ['scylla = scylla.cli:app_main']
    },
    version=scylla.__version__,
    description='Intelligent proxy pool for Humans™',
    long_description=long_description,
    author=scylla.__author__,
    author_email='wildcat.name@gmail.com',
    url='https://github.com/imWildCat/scylla',
    # download_url='https://github.com/imWildCat/scylla/archive/0.1.0.tar.gz',
    keywords=['proxy', 'api', 'scylla'],
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: Apache Software License'
    ],
    install_requires=required,
    include_package_data=True,
)
