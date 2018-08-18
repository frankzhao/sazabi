"""
Source build and installation script.
"""

from os import path, sep, walk
from setuptools import setup, find_packages

version = '0.0.1-dev'


def extract_requirements(filename):
    return open(filename, "r").read().split("\n")


def find_package_data(source, strip=''):
    pkg_data = []
    for root, dirs, files in walk(source):
        pkg_data += map(
            lambda f: path.join(root.replace(strip, '').lstrip(sep), f),
            files
        )
    return pkg_data


base_dir = path.dirname(__file__)

with open(path.join(base_dir, 'README.md')) as f:
    long_description = f.read()

install_requires = extract_requirements('requirements.txt')

setup(
    name='sazabi',
    version=version,
    description='Sazabi: A discord bot',
    long_description=long_description,
    license='MIT',
    url='https://github.com/frankzhao/sazabi',
    author='Frank Zhao',
    author_email='frank@frankzhao.net',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    scripts=['bin/sazabi'],
    install_requires=install_requires,
)
