from os.path import isfile
from sys import version_info

from setuptools import find_packages
from setuptools import setup


def requirements_for(version=None):
    suffix = '-py%s' % version if version is not None else ''
    pip_path = 'requirements%s.pip' % suffix

    if not isfile(pip_path):
        return set()

    with open(pip_path) as pip_file:
        requirements = set(line.strip() for line in pip_file)
    return requirements


def install_requires():
    return requirements_for() | requirements_for(version_info.major)


setup(
    name='GutenbergPy',
    version='0.1.2',
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
    install_requires=install_requires() )
