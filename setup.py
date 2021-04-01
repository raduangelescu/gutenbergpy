from os.path import isfile
from sys import version_info

from setuptools import find_packages
from setuptools import setup

setup(
    packages=find_packages(),
    package_data={'gutenbergpy.caches': ['*.sql']},
    include_package_data=True)