# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='aquarius',
    version='0.0.1',
    description='A package to read Aquarius csv data files into Python pandas dataframes',
    long_description=readme,
    author='John Franco Saraceno',
    author_email='saraceno@usgs.gov',
    url='https://github.com/onegneissguy/aquarius',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

