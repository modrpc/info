# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='order',
    version='0.1.0',
    description='Naver smartstore order processing',
    long_description=readme,
    author='modrpc',
    author_email='mv3142@gmail.com',
    url='https://github.com/modrpc/info/code/smartstore',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
