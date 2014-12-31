#!/usr/bin/env python
import os
import sys
from distutils.core import setup
import django_choices

classifiers = '''\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Operating System :: OS Independent
Topic :: Software Development :: Libraries :: Python Modules
'''.splitlines()

setup(
    name='django_choices',
    version=django_choices.__version__,
    author='David Krauth',
    author_email='dakrauth@gmail.com',
    url='',
    license='MIT',
    platforms=['any'],
    py_modules=['django_choices'],
    description=django_choices.__doc__,
    classifiers=classifiers,
    long_description=''''''
)