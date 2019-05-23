# -*- coding: utf-8 -*-

# Copyright (c) 2019 MassChallenge, Inc.

from setuptools import setup


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='add2cal',
    version='0.1.0',
    description='',
    long_description=readme,
    author='Shankar Ambady',
    author_email='shankar@masschallenge.org',
    url='https://github.com/masschallenge/add2cal',
    license=license,
    package='add2cal',
    install_requires=[
        'urllib3',
        'ics'
    ])
