# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='zuul-dashboard',
    version='0.0.1',
    url='https://github.com/pawelzny/zuul-dashboard',
    author='Paweł Zadrożny',
    author_email='pawel.zny@gmail.com',
    description='Custom dashboard for Zuul',
    packages=find_packages(exclude=('docs',)),
)
