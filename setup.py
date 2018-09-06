# -*- coding: utf-8 -*-

import re
import os

from setuptools import setup
from setuptools import find_packages


README_FILE = os.path.join(
    os.path.abspath(
        os.path.dirname(__file__),
    ),
    'README.md',
)


with open('pagium/__init__.py') as fp:
    __version__ = re.search(r"__version__\s*=\s*'(.*)'", fp.read(), re.M).group(1)


with open(README_FILE) as fp:
    __description__ = fp.read()


setup(
    name='pagium',
    version=__version__,
    url='https://github.com/pagium/pagium',
    packages=find_packages(include=('pagium',)),
    description='Selenium page object implementation',
    long_description=__description__,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'selenium',
        'pyhamcrest',
    ],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Natural Language :: Russian',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
