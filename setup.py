#!/usr/bin/env python

import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requires = [
    'Click==4.0',
    'python-gnupg==0.3.7',
    'requests==2.7.0',
]

version = ''
with open('sekrets/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

setup(
    name='sekrets',
    version=version,
    description='Encrypt files for multiple recipients with keybase.io + gpg',
    author='Ryan Greget',
    author_email='rgreget@gmail.com',
    url='https://github.com/AngryEgret/sekrets',
    py_modules=['sekrets'],
    install_requires= requires,
    entry_points='''
        [console_scripts]
        sekrets=sekrets.sekrets:cli
    ''',
    license='',
)
