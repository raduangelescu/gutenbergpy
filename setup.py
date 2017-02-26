from os.path import isfile
from sys import version_info

from setuptools import find_packages
from setuptools import setup




setup(
    name='GutenbergPy',
    version='0.1.7',
    author='Radu Angelescu',
    author_email='raduangelescu+pypi@gmail.com',
    packages=find_packages(),
    package_data={'gutenberg.caches': ['*.sql']},
    url='https://github.com/raduangelescu/gutenbergpy',
    download_url='http://pypi.python.org/pypi/GutenbergPy',
    license='LICENSE.txt',
    description='Library to create and interogate local cache for Project Gutenberg',
    long_description=open('README.rst').read(),
    include_package_data=True,
    install_requires=['future>=0.15.2','setuptools>=18.5','lxml>=3.2.0'] )
