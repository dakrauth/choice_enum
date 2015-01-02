#!/usr/bin/env python
import os
import sys
from distutils.core import setup
import choice_enum

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

with open('README.md') as fp:
    long_description = fp.read()


setup(
    name='choice_enum',
    version=choice_enum.__version__,
    author='David Krauth',
    author_email='dakrauth@gmail.com',
    url='https://github.com/dakrauth/choice_enum',
    license='MIT',
    platforms=['any'],
    py_modules=['choice_enum'],
    description=choice_enum.__doc__,
    classifiers=classifiers,
    long_description=long_description
)