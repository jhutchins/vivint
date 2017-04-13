from codecs import open
from os import path
from setuptools import setup, find_packages

import vivint

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vivint',
    version=vivint.__version__,
    description='Vivint homework assignment',
    long_description=long_description,
    author='Jeff Hutchins',
    author_email='complife@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['web.py'],
    entry_points = {
        'console_scripts': ['vivint=vivint.__main__'],
    },
    setup_requires=['pytest-runner'],
    tests_require=['coverage', 'pytest'],
)
