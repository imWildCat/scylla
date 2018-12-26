import io
import os

from setuptools import setup, find_packages

import scylla

here = os.path.abspath(os.path.dirname(__file__))
# Import the README and use it as the long-description.
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='scylla',
    python_requires='>=3.6.0',
    # If your package is a single module, use this instead of 'packages':
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
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
