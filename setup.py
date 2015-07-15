# -*- coding: utf-8 -*-

import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('tdfscrape/tdfscrape.py').read(),
    re.M
    ).group(1)


with open('README.md', 'rb') as f:
    long_descr = f.read().decode('utf-8')


setup(
    name='cmdline-bootstrap',
    packages=['tdfscrape'],
    entry_points={
        'console_scripts': ['tdfscrape=tdfscrape.tdfscrape:main']
        },
    version=version,
    description='Parses results from the Tour de France game at http://ifarm.nl/tdf.',
    long_description=long_descr,
    author='Brad Sokol',
    url='https://github.com/bradsokol/tdf-scrape',
    )
