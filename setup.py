#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dvh
import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='dvh',
    version=dvh.__version__,
    description='Small package for manipulating dose volume histograms in Python',
    long_description=readme + '\n\n' + history,
    author=dvh.__author__,
    author_email=dvh.__email__,
    url='https://github.com/randlet'
        '/dvh',
    packages=[
        'dvh',
    ],
    package_dir={'dvh':
                 'dvh'},
    include_package_data=True,
    install_requires=[
        'numpy',
    ],
    license="BSD",
    zip_safe=False,
    keywords='dvh',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
)
