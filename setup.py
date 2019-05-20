#!/usr/bin/env python3
# coding=utf-8

import sys
from distutils import core
from os.path import abspath, dirname

from setuptools import find_packages

__author__ = "Josef Kolář"

if sys.version_info < (3, 5):
    print('Run in python >= 3.5 please.', file=sys.stderr)
    exit(1)

base_path = abspath(dirname(__file__))


def setup():
    core.setup(
        name='litovel-minicup-live-service',
        version='1.0.0',
        description='Tornado server fro distributing live results from Litovel MINICUP',
        author='Josef Kolář',
        author_email='thejoeejoee@gmail.com',
        packages=find_packages(),
        install_requires=[
            'tornado==5.0.2',
            'vokativ',
            'gunicorn==19.8.1',
            'raven',
        ],
        entry_points={
            'console_scripts': [
                'litovel-minicup-live-service=minicup_live_service.app:main',
                'litovel-minicup-live-service-manage=minicup_model.manage:manage',
            ],
        },
        include_package_data=True,
    )


if __name__ == '__main__':
    setup()
